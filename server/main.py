import json

from typing import List
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from helpers.planner_helper.planner_helper_data_types import (
    LandmarksResponseModel,
    PlannerResponseModel,
    PlanDisambiguatorOutput,
    PlanDisambiguatorInput,
    LemmingTask,
    PlanningTask,
    Plan,
    LTLFormula,
    NL2LTLRequest,
    LTL2PDDLRequest,
    Translation,
)
from helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topq,
    get_planner_response_model_with_hash,
)
from helpers.common_helper.file_helper import (
    read_str_from_upload_file,
)
from helpers.plan_disambiguator_helper.selection_flow_helper import (
    get_selection_flow_output,
)
from helpers.common_helper.static_data_helper import app_description
from helpers.plan_disambiguator_helper.build_flow_helper import (
    get_build_flow_output,
)

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


def handle_flow_output(
    flow_output: PlanDisambiguatorOutput,
) -> PlanDisambiguatorOutput:
    if flow_output is None:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")
    return flow_output


def check_pddl_input(plan_disambiguator_input: PlanDisambiguatorInput) -> None:
    if not PlanDisambiguatorInput.check_domain_problem(
        plan_disambiguator_input
    ):
        raise HTTPException(
            status_code=400, detail="Bad Request: domain or problem is empty"
        )


@app.get("/")
def hello_lemming() -> str:
    return "Hello Lemming!"


@app.post("/file_upload")
async def file_upload(file: UploadFile = File(...)) -> str:
    file_contents = read_str_from_upload_file(file)
    return file_contents


@app.post("/import_domain/{domain_name}")
def import_domain(domain_name: str) -> LemmingTask:
    planning_task = PlanningTask(
        domain=open(f"./data/{domain_name}/domain.pddl").read(),
        problem=open(f"./data/{domain_name}/problem.pddl").read(),
    )

    try:
        plans = json.load(open(f"./data/{domain_name}/plans.json"))
        plans = [Plan.parse_obj(item) for item in plans]

    except Exception as e:
        print(e)
        plans = []

    try:
        prompt = json.load(open(f"./data/{domain_name}/prompt.json"))
        nl_prompts = [Translation.parse_obj(item) for item in prompt]

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
    if planning_task.domain is None or planning_task.problem is None:
        raise HTTPException(status_code=400, detail="Bad Request")

    landmarks = get_landmarks_by_landmark_category(
        planning_task, landmark_category
    )

    if landmarks is None:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")

    return LandmarksResponseModel(landmarks=landmarks)


@app.post("/get_plans")
async def get_plans(planning_task: PlanningTask) -> PlannerResponseModel:
    if (
        planning_task.domain is None
        or planning_task.problem is None
        or len(planning_task.domain) == 0
        or len(planning_task.problem) == 0
    ):
        raise HTTPException(
            status_code=400, detail="Bad Request: domain or problem is empty"
        )

    planning_result = get_plan_topq(planning_task)

    if planning_result is None:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")

    return get_planner_response_model_with_hash(planning_result)


@app.post("/generate_select_view")
def generate_select_view(
    plan_disambiguator_input: PlanDisambiguatorInput,
) -> PlanDisambiguatorOutput:
    check_pddl_input(plan_disambiguator_input)

    flow_output = get_selection_flow_output(
        plan_disambiguator_input.selection_infos,
        plan_disambiguator_input.landmarks,
        plan_disambiguator_input.domain,
        plan_disambiguator_input.problem,
        plan_disambiguator_input.plans,
        plan_disambiguator_input.selection_priority,
    )

    return handle_flow_output(flow_output)


@app.post("/generate_build_forward")
def generate_build_forward(
    plan_disambiguator_input: PlanDisambiguatorInput,
) -> PlanDisambiguatorOutput:
    check_pddl_input(plan_disambiguator_input)

    flow_output = get_build_flow_output(
        plan_disambiguator_input.selection_infos,
        plan_disambiguator_input.landmarks,
        plan_disambiguator_input.domain,
        plan_disambiguator_input.problem,
        plan_disambiguator_input.plans,
        True,
    )

    return handle_flow_output(flow_output)


@app.post("/generate_build_backward")
def generate_build_backward(
    plan_disambiguator_input: PlanDisambiguatorInput,
) -> PlanDisambiguatorOutput:
    check_pddl_input(plan_disambiguator_input)

    flow_output = get_build_flow_output(
        plan_disambiguator_input.selection_infos,
        plan_disambiguator_input.landmarks,
        plan_disambiguator_input.domain,
        plan_disambiguator_input.problem,
        plan_disambiguator_input.plans,
        False,
    )

    return handle_flow_output(flow_output)


@app.post("/generate_nl2ltl_integration")
def generate_nl2ltl_integration(
    plan_disambiguator_input: PlanDisambiguatorInput,
) -> PlanDisambiguatorOutput:
    return generate_select_view(plan_disambiguator_input)


@app.post("/nl2ltl")
def nl2ltl(request: NL2LTLRequest) -> List[LTLFormula]:
    _ = request

    # TODO: Call to NL2LTL
    ltl_formulas: List[LTLFormula] = [
        LTLFormula(
            user_prompt=request.utterance,
            formula="RespondedExistence Slack Gmail",
            description="If Slack happens at least once then Gmail has to happen or happened before Slack.",
            confidence=0.4,
        ),
        LTLFormula(
            user_prompt=request.utterance,
            formula="Response Slack Gmail",
            description="Whenever activity Slack happens, activity Gmail has to happen eventually afterward.",
            confidence=0.3,
        ),
        LTLFormula(
            user_prompt=request.utterance,
            formula="ExistenceTwo Slack",
            description="Slack will happen at least twice.",
            confidence=0.2,
        ),
    ]

    return ltl_formulas


@app.post("/ltl_compile")
def ltl_compile(request: LTL2PDDLRequest) -> LemmingTask:
    planning_task = PlanningTask(domain=request.domain, problem=request.problem)
    lemming_task = LemmingTask(planning_task=planning_task, plans=request.plans)

    # TODO: Compile to new planning task
    return lemming_task
