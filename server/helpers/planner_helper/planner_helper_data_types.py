from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any
from dacite import from_dict
from server.helpers.common_helper.hash_helper import get_list_hash
from server.helpers.nl2plan_helper.nl2ltl_helper import LTLFormula, CachedPrompt
from pydantic import BaseModel, validator
from watson_ai_planning.data_model.planning_types import PlanningResult


class Plan(BaseModel):
    actions: List[str] = []
    cost: int = 0
    plan_hash: Optional[str] = None


class Landmark(BaseModel):
    facts: List[str] = []
    disjunctive: bool = False
    first_achievers: List[str] = []


class SelectionInfo(BaseModel):
    selected_first_achiever: Optional[str] = ""
    selected_plan_hashes: Optional[List[str]] = []


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


class PlannerResponseModel(BaseModel):
    plans: List[Plan] = []

    @staticmethod
    def get_planning_results(model: PlannerResponseModel) -> PlanningResult:
        return from_dict(data_class=PlanningResult, data=model.dict())

    def set_plan_hashes(self) -> None:
        for plan in self.plans:
            plan.plan_hash = get_list_hash(plan.actions)


class LandmarksResponseModel(BaseModel):
    landmarks: List[Landmark] = []


class ChoiceInfo(BaseModel):
    landmark: Optional[Landmark] = None  # landmark
    max_num_plans: Optional[
        int
    ] = 0  # the maximum number of plans included in a first achiever
    action_name_plan_idx_map: Optional[
        Dict[str, List[int]]
    ] = (
        dict()
    )  # keys are first-achievers (or edges) available fore the next choice
    action_name_plan_hash_map: Optional[
        Dict[str, List[str]]
    ] = (
        dict()
    )  # keys are first-achievers (or edges) available fore the next choice
    nodes_with_multiple_out_edges: List[str] = []
    is_available_for_choice: bool = True


class PlanDisambiguatorInput(BaseModel):
    selection_priority: str
    selection_infos: List[SelectionInfo] = []
    landmarks: List[Landmark] = []
    plans: List[Plan]
    domain: str = ""
    problem: str = ""

    @staticmethod
    def check_domain_problem(input: PlanDisambiguatorInput) -> bool:
        return (
            input.domain is not None
            and len(input.domain) > 0
            and input.problem is not None
            and len(input.problem) > 0
        )

    @validator("selection_infos")
    def check_selected_landmarks(
        cls, v: List[SelectionInfo]
    ) -> Optional[List[SelectionInfo]]:
        if v is None:
            raise ValueError("selection_infos should not be None")
        return v

    @validator("landmarks")
    def check_landmarks(cls, v: List[Landmark]) -> Optional[List[Landmark]]:
        if v is None:
            raise ValueError("landmarks should not be None")
        return v

    @validator("plans")
    def check_plans(cls, v: List[Plan]) -> Optional[List[Plan]]:
        if v is None:
            raise ValueError("plans should not be None")
        if len(v) == 0:
            raise ValueError("The length of plans should be greater than 0")
        return v


class PlanDisambiguatorOutput(BaseModel):
    plans: List[Plan] = []
    choice_infos: List[ChoiceInfo] = []
    networkx_graph: Dict[str, Any] = {}
    first_achiever_edge_dict: Optional[Dict[str, Any]] = None
    node_plan_hashes_dict: Optional[Dict[str, List[str]]] = None
    edge_plan_hashes_dict: Optional[Dict[str, List[str]]] = None


class PlanningTask(BaseModel):
    domain: str
    problem: str
    num_plans: int = 2
    quality_bound: float = 1.0


class LemmingTask(BaseModel):
    planning_task: PlanningTask
    plans: List[Plan] = []
    nl_prompts: List[CachedPrompt] = []


class LTL2PDDLRequest(BaseModel):
    formulas: List[LTLFormula]
    plans: List[Plan]
    domain: str
    problem: str


class ToolCompiler(Enum):
    P4P = "p4p"
    LF2F = "lf2f"
