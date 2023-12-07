from typing import List
from planners.drivers.planner_driver_datatype import Plan, PlanningResult


def format_plan(actions: List[str]) -> List[str]:
    """
    returns formatted plan and a hash
    """
    formatted_actions: List[str] = list()
    for action in actions:
        terms = action.split(" ")
        formatted_terms: List[str] = list()
        for term in terms:
            if len(term) > 0:
                formatted_terms.append(term[:])
        if len(formatted_terms) > 0:
            formatted_actions.append(" ".join(formatted_terms))

    return formatted_actions


def format_plans(planning_results: PlanningResult) -> PlanningResult:
    formatted_plans: List[Plan] = list()
    for plan in planning_results.plans:
        formatted_plans.append(
            Plan(actions=format_plan(plan.actions), cost=plan.cost)
        )
    return PlanningResult(plans=formatted_plans)
