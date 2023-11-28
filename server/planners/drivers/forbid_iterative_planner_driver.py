from typing import List, Optional
import tempfile
from pathlib import Path
import forbiditerative
import subprocess
import sys
import json
from server.planners.drivers.planner_driver_datatype import PlanningResult, PlanningResultDict, PlanDict
from server.planners.drivers.planner_driver_helper import parse_planning_result

build_dir = Path(forbiditerative.__file__).parent / \
    "builds" / "release" / "bin"


def execute_forbid_iterative_planner(
    planner_name: str,
    domain: str,
    problem: str,
    num_plans: int,
    quality_bound: Optional[float] = None,
    timeout: Optional[int] = None,
    case_sensitive: Optional[bool] = False,
) -> PlanningResult:
    with tempfile.NamedTemporaryFile() as plan_temp, tempfile.NamedTemporaryFile() as domain_temp, tempfile.NamedTemporaryFile() as problem_temp:
        plan_file = Path(tempfile.gettempdir()) / plan_temp.name
        domain_file = Path(tempfile.gettempdir()) / domain_temp.name
        problem_file = Path(tempfile.gettempdir()) / problem_temp.name
        domain_file.write_text(domain)
        problem_file.write_text(problem)

        time_limit = []
        if timeout:
            time_limit.extend(["--overall-time-limit", str(timeout)])

        translator_options = ["--case-sensitive"] if case_sensitive else []

        proc = subprocess.run(
            [sys.executable, "-B", "-m", "forbiditerative.plan"]
            + ["--build", str(build_dir.absolute())]
            + ["--planner", planner_name]
            + [
                "--domain",
                str(domain_file.absolute()),
                "--problem",
                str(problem_file.absolute()),
            ]
            + ["--number-of-plans", str(num_plans)]
            + (
                ["--quality-bound", str(quality_bound)]
                if quality_bound is not None
                else []
            )
            + [
                "--symmetries",
                "--use-local-folder",
                "--clean-local-folder",
                "--plans-as-json",
            ]
            + time_limit
            + translator_options
            + ["--results-file", str(plan_file.absolute())]
        )
        planner_exit_code = proc.returncode
        result: PlanningResultDict = json.loads(plan_file.read_text())
        planning_result: PlanningResult = parse_planning_result(result)
        planning_result.planner_name = f"{planner_name}"
        planning_result.planner_exit_code = planner_exit_code
        return planning_result


def plan_to_text(plan: PlanDict) -> str:
    actions = ["(" + a + ")" for a in plan["actions"]]
    return "\n".join(actions) + "\n" + f"; cost = {plan.get('cost')} (unit cost)"


def get_plans_dot(domain: str, problem: str, plans: List[PlanDict]) -> str:
    """Execute the planner on the task, no search."""
    # a mapping from category to aliases recognized by the planner
    # each alias represents a large amount of settings.
    with tempfile.NamedTemporaryFile() as domain_temp, \
            tempfile.NamedTemporaryFile() as problem_temp:
        # We have to read and write to files because the planner is CLI oriented.
        graph_file = Path(tempfile.gettempdir()) / "graph0.dot"
        plans_path = Path(tempfile.gettempdir()) / "plans"
        domain_file = Path(tempfile.gettempdir()) / domain_temp.name
        problem_file = Path(tempfile.gettempdir()) / problem_temp.name
        domain_file.write_text(domain)
        problem_file.write_text(problem)
        if not (plans_path.is_dir()):
            plans_path.mkdir()
        counter = 1
        for plan in plans:
            plan_file = Path(plans_path / f'sas_plan.{counter}')
            plan_file.write_text(plan_to_text(plan))
            counter += 1

        counter -= 1
        subprocess.run(
            [sys.executable, "-B", "-m", "driver.main"]
            + ["--build", str(build_dir.absolute())]
            + [str(domain_file.absolute()), str(problem_file.absolute())]
            + ["--search", f'forbid_iterative(reformulate=NONE,read_plans_and_dump_graph=true,external_plans_path={plans_path},number_of_plans_to_read={counter})'], cwd=Path(tempfile.gettempdir())
        )
        return graph_file.read_text()
