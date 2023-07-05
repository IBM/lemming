"""Wrapper to the SymK planner."""
import glob
import json
import re
import subprocess
import tempfile
from typing import Dict, Optional, Any

import inspect
from pathlib import Path

from watson_ai_planning.data_model import PlanningResult
from watson_ai_planning.planner.utils import (
    PlanningResultDict,
    parse_planning_result,
)

from helpers.planner_helper.planner_helper_data_types import PlanningTask
from server.planners.base import Planner

PLANNERS_ROOT = Path(
    inspect.getframeinfo(inspect.currentframe()).filename
).parent
SERVER_ROOT = PLANNERS_ROOT.parent

DEFAULT_BIN_SYMK_PATH = (
    SERVER_ROOT / "third_party" / "symk" / "fast-downward.py"
).absolute()
DEFAULT_K = 10
DEFAULT_QUALITY = 2
DEFAULT_HEURISTIC = f"(plan_selection=top_k(num_plans={str(DEFAULT_K)},dump_plans=false),quality={str(DEFAULT_QUALITY)})"
DEFAULT_SEARCH = f"symq-bd({DEFAULT_HEURISTIC})"


def create_plan_from_file(plan_file: Path) -> Dict[Any, Any]:
    with open(plan_file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    actions = [x[1:-1] for x in content if x.startswith("(")]
    ret = {"actions": actions}
    cost = [x for x in content if not x.startswith("(") and "cost" in x]
    if len(cost) >= 1:
        q = re.findall(r"; cost = (\d+)", cost[0], re.M)
        ret["cost"] = q[0]
    return ret


def _parse_planning_result(plan_file_prefix_name: str) -> str:
    """Parse plans and create a json."""
    plan_file_name = f"{plan_file_prefix_name}*"
    plan_files = glob.glob(plan_file_name)

    unique_plans = set()
    plans = []
    for fplan in plan_files:
        plan = create_plan_from_file(Path(fplan))
        if plan is not None:
            actions_tuple = tuple(plan["actions"])
            if actions_tuple not in unique_plans:
                unique_plans.add(actions_tuple)
                plans.append(plan)
    return json.dumps({"plans": plans})


class SymKPlanner(Planner):
    """Wrapper to SymKPlanner."""

    def __init__(
        self,
        bin_path: Path = DEFAULT_BIN_SYMK_PATH,
    ) -> None:
        """
        Initialize the planner.

        :param bin_path: path to the executable.
        """
        assert bin_path.exists()
        self._bin_path = bin_path

    @property
    def bin_path(self) -> Path:
        """Return path to the binary."""
        return self._bin_path

    def plan(
        self, planning_task: PlanningTask, **options: Dict[str, str]
    ) -> Optional[PlanningResult]:
        """
        Compute a set of plans.

        :param planning_task: the planning task.
        :param options: options for the planner.
        :return: the plan.
        """
        with tempfile.NamedTemporaryFile(
            delete=False
        ) as plan_temp, tempfile.NamedTemporaryFile() as domain_temp, tempfile.NamedTemporaryFile() as problem_temp:
            # We have to read and write to files because the planner is CLI
            # oriented.
            plan_file = Path(tempfile.gettempdir()) / plan_temp.name
            domain_file = Path(tempfile.gettempdir()) / domain_temp.name
            problem_file = Path(tempfile.gettempdir()) / problem_temp.name
            domain_file.write_text(planning_task.domain)
            problem_file.write_text(planning_task.problem)
            self._call_planner(
                domain_file,
                problem_file,
                planning_task.num_plans,
                planning_task.quality_bound,
                plan_file,
            )
            json_plans = _parse_planning_result(str(plan_file))
            result: PlanningResultDict = json.loads(str(json_plans))

            for plan in result["plans"]:
                plan["cost"] = int(plan["cost"])
            return parse_planning_result(result)

    def _call_planner(
        self,
        domain_path: Path,
        problem_path: Path,
        num_plans: int,
        quality: float,
        plans_path: Path,
    ) -> None:
        """Call the planner."""
        cmd = [
            self.bin_path,
            "--plan-file",
            str(plans_path.absolute()),
            str(domain_path.absolute()),
            str(problem_path.absolute()),
            "--search",
            f"symq-bd(plan_selection=top_k(num_plans={str(num_plans)},dump_plans=false),quality={str(quality)})",
        ]
        subprocess.check_call(cmd)
