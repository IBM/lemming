import json

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
)
from helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topq,
    get_planner_response_model_with_hash,
)
from helpers.common_helper.file_helper import (
    read_str_from_upload_file,
    convert_json_str_to_dict,
)
from helpers.plan_disambiguator_helper.selection_flow_helper import (
    get_selection_flow_output,
)
from helpers.common_helper.static_data_helper import app_description
from helpers.plan_disambiguator_helper.build_flow_helper import (
    get_build_forward_flow_output,
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
        plans = [
            Plan(actions=item["actions"], cost=item["cost"]) for item in plans
        ]

    except Exception as e:
        print(e)
        plans = []

    new_lemming_task = LemmingTask(planning_task=planning_task, plans=plans)
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


@app.post("/generate_select_view/object")
def generate_select_view(
    plan_disambiguator_input: PlanDisambiguatorInput,
) -> PlanDisambiguatorOutput:
    if not PlanDisambiguatorInput.check_domain_problem(
        plan_disambiguator_input
    ):
        raise HTTPException(
            status_code=400, detail="Bad Request: domain or problem is empty"
        )

    flow_output = get_selection_flow_output(
        plan_disambiguator_input.selection_infos,
        plan_disambiguator_input.landmarks,
        plan_disambiguator_input.domain,
        plan_disambiguator_input.problem,
        plan_disambiguator_input.plans,
    )

    if flow_output is None:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")

    return flow_output


@app.post("/generate_select_view_with_files/files")
def generate_select_view_with_files(
    domain_file: UploadFile,
    problem_file: UploadFile,
    plan_disambiguator_input_json_file: UploadFile,
) -> PlanDisambiguatorOutput:
    domain = read_str_from_upload_file(domain_file)
    problem = read_str_from_upload_file(problem_file)

    if (
        domain is None
        or problem is None
        or len(domain) == 0
        or len(problem) == 0
    ):
        raise HTTPException(
            status_code=400, detail="Bad Request: domain or problem is empty"
        )
    flow_input_json_str = read_str_from_upload_file(
        plan_disambiguator_input_json_file
    )

    if flow_input_json_str is None or len(flow_input_json_str) == 0:
        raise HTTPException(
            status_code=400,
            detail="Bad Request: selection_flow_input_json_file is empty",
        )

    flow_input = PlanDisambiguatorInput.parse_obj(
        convert_json_str_to_dict(flow_input_json_str)
    )
    flow_output = get_selection_flow_output(
        flow_input.selection_infos,
        flow_input.landmarks,
        domain,
        problem,
        flow_input.plans,
    )

    if flow_output is None:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")

    return flow_output


@app.post("/generate_build_forward/object")
def generate_build_forward(
    plan_disambiguator_input: PlanDisambiguatorInput,
) -> PlanDisambiguatorOutput:
    if not PlanDisambiguatorInput.check_domain_problem(
        plan_disambiguator_input
    ):
        raise HTTPException(
            status_code=400, detail="Bad Request: domain or problem is empty"
        )

    flow_output = get_build_forward_flow_output(
        plan_disambiguator_input.selection_infos,
        plan_disambiguator_input.landmarks,
        plan_disambiguator_input.domain,
        plan_disambiguator_input.problem,
        plan_disambiguator_input.plans,
    )

    if flow_output is None:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")

    return flow_output


@app.post("/generate_build_forward_with_files/files")
def generate_build_forward_with_files(
    domain_file: UploadFile,
    problem_file: UploadFile,
    plan_disambiguator_input_json_file: UploadFile,
) -> PlanDisambiguatorOutput:
    domain = read_str_from_upload_file(domain_file)
    problem = read_str_from_upload_file(problem_file)

    if (
        domain is None
        or problem is None
        or len(domain) == 0
        or len(problem) == 0
    ):
        raise HTTPException(
            status_code=400, detail="Bad Request: domain or problem is empty"
        )
    flow_input_json_str = read_str_from_upload_file(
        plan_disambiguator_input_json_file
    )

    if flow_input_json_str is None or len(flow_input_json_str) == 0:
        raise HTTPException(
            status_code=400,
            detail="Bad Request: selection_flow_input_json_file is empty",
        )

    flow_input = PlanDisambiguatorInput.parse_obj(
        convert_json_str_to_dict(flow_input_json_str)
    )
    flow_output = get_build_forward_flow_output(
        flow_input.selection_infos,
        flow_input.landmarks,
        domain,
        problem,
        flow_input.plans,
    )

    if flow_output is None:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")

    return flow_output


# @app.route("/generate_build_backward", methods=["POST"])
# def generate_build_backward() -> Any:
#     viz: Any = None
#     return jsonify(viz)


# @app.route("/generate_landmarks_view", methods=["POST"])
# def generate_landmarks_view() -> Any:
#     viz: Any = None
#     return jsonify(viz)
