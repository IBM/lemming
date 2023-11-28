from planners.drivers.planner_driver_datatype import (
    Plan, Plan, PlanningResultDict, PlanningResult
)


def parse_planning_result(planning_result: PlanningResultDict) -> PlanningResult:
    if planning_result and 'plans' in planning_result:
        return PlanningResult(plans=[Plan(actions=plan['actions'], cost=int(plan.get('cost'))) for plan in planning_result['plans']])
    else:
        return PlanningResult(plans=[])
