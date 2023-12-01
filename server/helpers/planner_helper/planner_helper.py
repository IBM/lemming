from typing import Any, Dict, List, Optional

from helpers.common_helper.exception_handler import planner_exception_handler
from helpers.common_helper.str_helper import format_plans
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    PlanningTask,
)
from planners.drivers.forbid_iterative_planner_driver import (
    execute_forbid_iterative_planner,
    get_plans_dot,
)
from planners.drivers.landmark_driver import get_landmarks
from planners.drivers.planner_driver_datatype import PlanDict, PlanningResult


def as_dict(obj: object) -> Dict[str, Any]:
    output = {}
    for name, value in obj.__dict__.items():
        if name == "__pydantic_initialised__":
            continue
        if hasattr(type(value), "__pydantic_initialised__"):
            value = as_dict(value)
        output[name] = value
    return output


@planner_exception_handler
def get_plan_topk(planning_task: PlanningTask) -> Optional[PlanningResult]:
    return format_plans(
        execute_forbid_iterative_planner(
            planner_name="topk",
            domain=planning_task.domain,
            problem=planning_task.problem,
            num_plans=planning_task.num_plans,
            quality_bound=planning_task.quality_bound,
        )
    )


@planner_exception_handler
def get_landmarks_by_landmark_category(
    planning_task: PlanningTask, landmark_category: str
) -> List[Landmark]:
    return get_landmarks(
        landmark_category,
        planning_task.domain,
        planning_task.problem,
    )


@planner_exception_handler
def get_dot_graph_str(
    planning_task: PlanningTask, planning_results: PlanningResult
) -> str:
    planning_dicts = list(
        map(
            lambda plan: as_dict(
                PlanDict(actions=plan.actions, cost=plan.cost)
            ),
            planning_results.plans,
        )
    )
    dot_graph_str: str = get_plans_dot(
        planning_task.domain,
        planning_task.problem,
        planning_dicts,
    )
    return dot_graph_str
