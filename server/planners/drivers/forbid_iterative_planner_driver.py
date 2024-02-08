from typing import List, Optional
from pathlib import Path
from forbiditerative import planners
import tempfile

from server.planners.drivers.planner_driver_datatype import PlanningResult, Plan


def execute_forbid_iterative_planner(
    planner_name: str,
    domain: str,
    problem: str,
    num_plans: int,
    quality_bound: Optional[float] = None,
) -> PlanningResult:
    with (
        tempfile.NamedTemporaryFile() as domain_temp,
        tempfile.NamedTemporaryFile() as problem_temp,
    ):
        domain_file = Path(tempfile.gettempdir()) / domain_temp.name
        problem_file = Path(tempfile.gettempdir()) / problem_temp.name
        domain_file.write_text(domain)
        problem_file.write_text(problem)

        result = planners.plan_unordered_topq(
            domain_file=domain_file,
            problem_file=problem_file,
            quality_bound=quality_bound,
            number_of_plans_bound=num_plans,
        )
        planning_result: PlanningResult = PlanningResult(**result)
        planning_result.planner_name = f"{planner_name}"

        return planning_result


def get_plans_dot(domain: str, problem: str, plans: List[Plan]) -> str:
    with (
        tempfile.NamedTemporaryFile() as domain_temp,
        tempfile.NamedTemporaryFile() as problem_temp,
    ):
        domain_file = Path(tempfile.gettempdir()) / domain_temp.name
        problem_file = Path(tempfile.gettempdir()) / problem_temp.name
        domain_file.write_text(domain)
        problem_file.write_text(problem)

        dot_txt: str = planners.get_dot(
            domain_file=domain_file,
            problem_file=problem_file,
            plans=[plan.actions for plan in plans],
        )
        return dot_txt
