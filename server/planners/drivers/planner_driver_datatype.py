from typing import List, Optional
from pydantic.dataclasses import dataclass


@dataclass
class PlanDict:
    actions: List[str]
    cost: Optional[int]


@dataclass
class PlanningResultDict:
    plans: List[PlanDict]


@dataclass
class PlanAction:
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
