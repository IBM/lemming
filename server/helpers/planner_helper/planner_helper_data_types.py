from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from pydantic import BaseModel, validator
from dacite import from_dict
from watson_ai_planning.data_model.planning_types import PlanningResult
from helpers.common_helper.hash_helper import get_list_hash


class Plan(BaseModel):
    actions: List[str] = []
    cost: int = 0
    plan_hash: Optional[str] = None


class Landmark(BaseModel):
    facts: List[str] = []
    disjunctive: bool = False
    first_achievers: List[str] = []


class SelelctionInfo(BaseModel):
    # facts: Optional[List[str]] = []
    # disjunctive: Optional[bool] = False
    selected_first_achiever: Optional[str] = ""
    selected_plan_hashes: Optional[List[str]] = []


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
    landmark: Optional[Landmark] = None
    max_num_plans: Optional[int] = None
    action_name_plan_idx_map: Optional[Dict[str, List[int]]] = None
    action_name_plan_hash_map: Optional[Dict[str, List[str]]] = None
    node_with_multiple_out_edges: Optional[str] = None
    is_available_for_choice: bool = True


class PlanDisambiguatorInput(BaseModel):
    selection_infos: List[SelelctionInfo] = []
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
        cls, v: List[SelelctionInfo]
    ) -> Optional[List[SelelctionInfo]]:
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
    edge_plan_hashes_dict: Optional[Dict[Tuple[str, str], List[str]]] = None


class PlanningTask(BaseModel):
    domain: str
    problem: str
    num_plans: int = 2
    quality_bound: float = 1.0


class Translation(BaseModel):
    utterance: str
    paraphrases: List[str]
    declare: List[str]


class LemmingTask(BaseModel):
    planning_task: PlanningTask
    plans: List[Plan] = []
    nl_prompts: List[Translation] = []


class NL2LTLRequest(BaseModel):
    utterance: str


class LTLFormula(BaseModel):
    user_prompt: str
    formula: str
    description: str
    confidence: float


class LTL2PDDLRequest(BaseModel):
    formulas: List[LTLFormula]
    plans: List[Plan]
    domain: str
    problem: str
