from typing import Optional
import tempfile
from pathlib import Path
import forbiditerative
import subprocess
import sys
import json
from server.planners.drivers.planner_driver_datatype import PlanningResult, PlanningResultDict
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
