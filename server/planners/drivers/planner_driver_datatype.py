from typing import List, Optional, TypedDict
from dataclasses import dataclass


class PlanDict(TypedDict):
    actions: List[str]
    cost: Optional[int]


class PlanningResultDict(TypedDict):
    plans: List[PlanDict]


class PlanAction(TypedDict, total=False):
    action_name: str
    parameters: List[str]
    metric: float


@dataclass
class Plan:
    actions: List[str]
    cost: int


@dataclass
class PlanningResult:
    plans: List[Plan]
