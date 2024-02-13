import functools
import json
import sys
from pathlib import Path
from typing import List, Dict, cast

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pddl.formatter import domain_to_string, problem_to_string

from helpers.common_helper.static_data_helper import app_description
from helpers.nl2plan_helper.utils import temporary_directory
from helpers.nl2plan_helper.ltl2plan_helper import (
    compile_instance,
    get_goal_formula,
)
from helpers.nl2plan_helper.manage_formulas import (
    get_formulas_from_matched_formulas,
)
from helpers.nl2plan_helper.nl2ltl_helper import (
    NL2LTLRequest,
    prompt_builder,
    LTLFormula,
)
from helpers.plan_disambiguator_helper.build_flow_helper import (
    get_build_flow_output,
)
from helpers.nl2plan_helper.nl2ltl_helper import CachedPrompt
from helpers.planner_helper.planner_helper_data_types import (
    LemmingTask,
    PlanDisambiguatorInput,
    PlanDisambiguatorOutput,
    PlanningTask,
    ToolCompiler,
    Plan,
    LTL2PDDLRequest,
)
from helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topk,
)
from helpers.common_helper.file_helper import (
    read_str_from_upload_file,
)
from helpers.plan_disambiguator_helper.selection_flow_helper import (
    get_selection_flow_output,
)
from planners.drivers.landmark_driver_datatype import LandmarksResponseModel
from planners.drivers.planner_driver_datatype import PlanningResult

try:
    from nl2ltl.declare.base import Template
    from nl2ltl import translate
    from nl2ltl.engines.gpt.core import GPTEngine, Models
    from pddl.parser.domain import DomainParser
    from pddl.parser.problem import ProblemParser
    from planners.symk import SymKPlanner
except ImportError as e:
    raise ImportError(e)

FILEPATH = Path(__file__).parent.resolve()

app = FastAPI(
    title="Lemming",
    description=app_description,
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def requires_optional(fn):
    @functools.wraps(fn)
    def wrapper_decor(*args, **kwargs):
        if "rasa" not in sys.modules:
            raise ModuleNotFoundError(
                f"Rasa is required to instantiate {fn.__name__}"
            )
        return fn(*args, **kwargs)

    return wrapper_decor


@app.get("/")
def hello_lemming() -> str:
    return "Hello Lemming!"


@app.post("/file_upload")
async def file_upload(file: UploadFile = File(...)) -> str:
    file_contents = read_str_from_upload_file(file)
    return file_contents


@app.post("/import_domain/{domain_name}")
def import_domain(domain_name: str) -> LemmingTask:
    path_to_domain_file = Path.joinpath(
        FILEPATH, f"data/{domain_name}/domain.pddl"
    ).resolve()
    path_to_problem_file = Path.joinpath(
        FILEPATH, f"data/{domain_name}/problem.pddl"
    ).resolve()

    planning_task = PlanningTask(
        domain=open(path_to_domain_file).read(),
        problem=open(path_to_problem_file).read(),
    )

    try:
        path_to_plan_file = Path.joinpath(
            FILEPATH, f"data/{domain_name}/plans.json"
        ).resolve()

        plans = json.load(open(path_to_plan_file))
        plans = [Plan.model_validate(item) for item in plans]

    except Exception as e:
        print(e)
        plans = []

    try:
        path_to_prompt_file = Path.joinpath(
            FILEPATH, f"data/{domain_name}/prompt.json"
        ).resolve()

        prompt = json.load(open(path_to_prompt_file))
        nl_prompts = [CachedPrompt.model_validate(item) for item in prompt]

    except Exception as e:
        print(e)
        nl_prompts = []

    new_lemming_task = LemmingTask(
        planning_task=planning_task, plans=plans, nl_prompts=nl_prompts
    )
    return new_lemming_task


@app.post("/get_landmarks/{landmark_category}")
async def get_landmarks(
    landmark_category: str,
    planning_task: PlanningTask,
) -> LandmarksResponseModel:
    landmarks = get_landmarks_by_landmark_category(
        planning_task, landmark_category
    )

    if landmarks is None:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")

    return LandmarksResponseModel(landmarks=landmarks)


@app.post("/get_plans")
async def get_plans(planning_task: PlanningTask) -> PlanningResult:
    planning_result = get_plan_topk(planning_task)

    if planning_result is None:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")

    return planning_result


@app.post("/generate_select_view")
def generate_select_view(
    plan_disambiguator_input: PlanDisambiguatorInput,
) -> PlanDisambiguatorOutput:
    plan_disambiguator_output, _, _ = get_selection_flow_output(
        plan_disambiguator_input.selection_infos,
        plan_disambiguator_input.landmarks,
        plan_disambiguator_input.domain,
        plan_disambiguator_input.problem,
        plan_disambiguator_input.plans,
        plan_disambiguator_input.selection_priority,
    )
    return plan_disambiguator_output


@app.post("/generate_build_forward")
def generate_build_forward(
    plan_disambiguator_input: PlanDisambiguatorInput,
) -> PlanDisambiguatorOutput:
    plan_disambiguator_output, _, _ = get_build_flow_output(
        plan_disambiguator_input.selection_infos,
        plan_disambiguator_input.landmarks,
        plan_disambiguator_input.domain,
        plan_disambiguator_input.problem,
        plan_disambiguator_input.plans,
        True,
    )
    return plan_disambiguator_output


@app.post("/generate_build_backward")
def generate_build_backward(
    plan_disambiguator_input: PlanDisambiguatorInput,
) -> PlanDisambiguatorOutput:
    plan_disambiguator_output, _, _ = get_build_flow_output(
        plan_disambiguator_input.selection_infos,
        plan_disambiguator_input.landmarks,
        plan_disambiguator_input.domain,
        plan_disambiguator_input.problem,
        plan_disambiguator_input.plans,
        False,
    )
    return plan_disambiguator_output


@requires_optional
@app.post("/generate_nl2ltl_integration")
def generate_nl2ltl_integration(
    plan_disambiguator_input: PlanDisambiguatorInput,
) -> PlanDisambiguatorOutput:
    return generate_select_view(plan_disambiguator_input)


@requires_optional
@app.post("/nl2ltl", response_model=None)
async def nl2ltl(request: NL2LTLRequest) -> List[LTLFormula]:
    domain_name = request.domain_name
    if domain_name:
        path_to_prompt_file = Path.joinpath(
            FILEPATH, f"data/{domain_name}/prompt.json"
        ).resolve()
        custom_prompt = prompt_builder(prompt_path=path_to_prompt_file)
    else:
        raise NotImplementedError

    with temporary_directory() as tmp_dir:
        tmp_file = Path(tmp_dir) / "tmp.json"
        tmp_file = tmp_file.resolve()
        tmp_file.write_text(custom_prompt, encoding="utf-8")

        engine = GPTEngine(model=Models.DAVINCI3.value, prompt=tmp_file)

    utterance = request.utterance
    matched_formulas: Dict[Template, float] = cast(
        Dict[Template, float], translate(utterance, engine)
    )
    ltl_formulas: List[LTLFormula] = get_formulas_from_matched_formulas(
        utterance, matched_formulas
    )
    if not ltl_formulas:
        raise HTTPException(status_code=422, detail="Unprocessable Utterance")

    return ltl_formulas


@requires_optional
@app.post("/ltl_compile/{tool}")
async def ltl_compile(
    request: LTL2PDDLRequest, tool: ToolCompiler
) -> LemmingTask:
    domain_parser = DomainParser()
    problem_parser = ProblemParser()

    domain = domain_parser(request.planning_task.domain)
    problem = problem_parser(request.planning_task.problem)
    goal = get_goal_formula(request.formulas, problem.goal, tool)

    compiled_domain, compiled_problem = compile_instance(
        domain, problem, goal, tool
    )
    planning_task = PlanningTask(
        domain=domain_to_string(compiled_domain),
        problem=problem_to_string(compiled_problem),
        num_plans=request.planning_task.num_plans,
        quality_bound=request.planning_task.quality_bound,
    )

    # Planning with SymK planner
    symk_planner = SymKPlanner()

    planning_result: PlanningResult = symk_planner.plan(planning_task)
    plans = planning_result.plans
    lemming_task = LemmingTask(planning_task=planning_task, plans=plans)

    return lemming_task
