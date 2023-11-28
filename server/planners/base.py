"""Interface for planner wrappers."""
from abc import ABC, abstractmethod
from typing import Dict, Optional

from server.planners.drivers.planner_driver_datatype import PlanningResult, PlanningTask


class Planner(ABC):  # pylint: disable=too-few-public-methods
    """Interface for planner wrappers."""

    @abstractmethod
    def plan(
        self, planning_task: PlanningTask, **options: Dict[str, str]
    ) -> Optional[PlanningResult]:
        """
        Find a plan.

        :param planning_task: the planning task.
        :param options: a dictionary of options.
        :return: a set of plans.
        """
