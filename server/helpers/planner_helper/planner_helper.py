from dataclasses import asdict
from typing import List, Optional
from watson_ai_planning.blocks.topq.iterative_unordered_topq import (
    IterativeUnorderedTopQ,
)
from watson_ai_planning.data_model import PlanningTask
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    PlannerResponseModel,
)
from watson_ai_planning.planner.fi import get_landmarks, get_plans_dot
from helpers.common_helper.str_helper import format_plans
from helpers.common_helper.exception_handler import planner_exception_handler
from watson_ai_planning.data_model.planning_types import PlanningResult
from helpers.common_helper.hash_helper import get_list_hash


def get_planner_response_model_with_hash(
    planning_result: PlanningResult,
) -> PlannerResponseModel:
    planner_response_model = PlannerResponseModel.parse_obj(
        asdict(planning_result)
    )

    for plan in planner_response_model.plans:
        plan.plan_hash = get_list_hash(plan.actions)

    return planner_response_model


@planner_exception_handler
def get_plan_topq(planning_task: PlanningTask) -> Optional[PlanningResult]:
    return format_plans(
        IterativeUnorderedTopQ().run(planning_task=planning_task)
    )


@planner_exception_handler
def get_landmarks_by_landmark_category(
    planning_task: PlanningTask, landmark_category: str
) -> List[Landmark]:
    landmarks = list(
        map(
            lambda result: Landmark.parse_obj(asdict(result)),
            get_landmarks(
                landmark_category,
                planning_task.domain,
                planning_task.problem,
            ),
        )
    )

    return list(
        map(
            lambda landmark: Landmark(
                facts=landmark.facts,
                disjunctive=landmark.disjunctive,
                first_achievers=list(
                    map(
                        lambda first_achiever: first_achiever.strip(),
                        landmark.first_achievers,
                    )
                ),
            ),
            landmarks,
        )
    )


@planner_exception_handler
def get_dot_graph_str(
    planning_task: PlanningTask, planning_results: PlanningResult
) -> str:
    planning_results_dict = asdict(planning_results)
    dot_graph_str: str = get_plans_dot(
        planning_task.domain,
        planning_task.problem,
        planning_results_dict.get("plans"),
    )
    return dot_graph_str
