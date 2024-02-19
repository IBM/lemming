from __future__ import annotations
from enum import Enum
import sys
from typing import Dict, List, Optional, Any, Tuple
from pydantic import BaseModel, field_validator, model_validator

from server.helpers.nl2plan_helper.nl2ltl_helper import LTLFormula, CachedPrompt

from server.planners.drivers.planner_driver_datatype import Plan
from server.planners.drivers.landmark_driver_datatype import Landmark

from fastapi import HTTPException


class PlanningTask(BaseModel):
    """The planning problem to solve."""

    domain: str = ""
    """The PDDL domain"""
    problem: str = ""
    """The PDDL problem"""
    num_plans: int = 1
    """The overall number of plans. Used in TopK or TopQ planners."""
    """TopQ planners may return up to `num_plans`."""
    quality_bound: float = 1.0
    """A relative (to an optimal plan cost) bound on the plans"""
    """quality (>= 1.0). Used in TopQ planners. """
    timeout: Optional[int] = None
    """The overall time limit (in seconds) on planner execution."""
    case_sensitive: Optional[bool] = False
    """Whether to treat PDDL as case-sensitive"""
    action_name_prefix_preserve: Optional[str] = None

    @model_validator(mode="after")
    def check_for_none(self) -> PlanningTask:
        if (
            self.domain == ""
            or self.problem == ""
            or len(self.domain) == 0
            or len(self.problem) == 0
        ):
            raise HTTPException(
                status_code=400,
                detail="Bad Request: domain or problem is empty",
            )

        return self


class SelectionInfo(BaseModel):
    selected_first_achiever: str = ""
    selected_edge: Optional[Tuple[str, str]] = None
    selected_plan_hashes: List[str] = []


class SelectionPriority(Enum):
    MAX_PLANS = "MAX_PLANS"
    MIN_PLANS = "MIN_PLANS"
    RANDOM = "RANDOM"
    INIT_FORWARD = "INIT_FORWARD"
    GOAL_BACKWARD = "GOAL_BACKWARD"


class LandmarkCategory(Enum):
    EXHAUST = "exhaust"
    H1 = "h1"
    H2 = "h2"
    RWH = "rhw"
    ZG = "zg"


class ChoiceInfo(BaseModel):
    landmark: Optional[Landmark] = None  # landmark
    # the maximum number of plans included in a first achiever
    max_num_plans: int = 0
    # keys are first-achievers (or edges) available for the next choice
    action_name_plan_idx_map: Dict[str, List[int]] = dict()
    # keys are first-achievers (or edges) available for the next choice
    action_name_plan_hash_map: Dict[str, List[str]] = dict()
    nodes_with_multiple_out_edges: List[str] = []
    is_available_for_choice: bool = True
    distance_to_init: int = sys.maxsize
    distance_to_end: int = sys.maxsize


class PlanDisambiguatorInput(BaseModel):
    selection_priority: Optional[str]
    selection_infos: List[SelectionInfo] = []
    landmarks: List[Landmark] = []
    plans: List[Plan]
    domain: str = ""
    problem: str = ""

    @model_validator(mode="after")
    def check_domain_problem(self) -> PlanDisambiguatorInput:
        if (
            self.domain is None
            or len(self.domain) == 0
            or self.problem is None
            or len(self.problem) == 0
        ):
            raise HTTPException(
                status_code=400,
                detail="Bad Request: domain or problem is empty",
            )

        return self

    @field_validator("selection_infos")
    @classmethod
    def check_selected_landmarks(
        cls, v: List[SelectionInfo]
    ) -> Optional[List[SelectionInfo]]:
        if v is None:
            raise ValueError("selection_infos should not be None")
        return v

    @field_validator("landmarks")
    @classmethod
    def check_landmarks(cls, v: List[Landmark]) -> Optional[List[Landmark]]:
        if v is None:
            raise ValueError("landmarks should not be None")
        return v

    @field_validator("plans")
    @classmethod
    def check_plans(cls, v: List[Plan]) -> Optional[List[Plan]]:
        if v is None:
            raise ValueError("plans should not be None")
        if len(v) == 0:
            raise ValueError("The length of plans should be greater than 0")
        return v


class PlanDisambiguationView(Enum):
    SELECT = "SELECT"
    BUILD_FORWARD = "BUILD_FORWARD"
    BUILD_BACKWARD = "BUILD_BACKWARD"


class PlanDisambiguatorOutput(BaseModel):
    plans: List[Plan] = []
    choice_infos: List[ChoiceInfo] = []
    networkx_graph: Dict[str, Any] = {}
    first_achiever_edge_dict: Dict[str, Any] = {}
    node_plan_hashes_dict: Dict[str, List[str]] = {}
    edge_plan_hashes_dict: Dict[str, List[str]] = {}

    @model_validator(mode="after")
    def check_for_none(self) -> PlanDisambiguatorOutput:
        if self is None:
            raise HTTPException(status_code=422, detail="Unprocessable Entity")
        return self

    def get_plan_costs(self) -> List[int]:
        return list(map(lambda plan: plan.cost, self.plans))


class LemmingTask(BaseModel):
    planning_task: PlanningTask
    plans: List[Plan] = []
    nl_prompts: List[CachedPrompt] = []


class LTL2PDDLRequest(BaseModel):
    formulas: List[LTLFormula]
    plans: List[Plan]
    planning_task: PlanningTask

    @model_validator(mode="after")
    def check_for_none(self) -> LTL2PDDLRequest:
        if (
            self.planning_task is None
            or self.planning_task.domain is None
            or self.planning_task.problem is None
            or self.formulas is None
        ):
            raise HTTPException(status_code=400, detail="Bad Request")

        return self


class ToolCompiler(Enum):
    P4P = "p4p"
    LF2F = "lf2f"
