from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel

import enum


class PlanningTask(BaseModel):
    domain: str
    problem: str


class Plan(BaseModel):
    steps: List[str]
    cost: float


class LemmingTask(BaseModel):
    planning_task: PlanningTask
    plans: List[Plan]


class LandmarkTypes(enum.Enum):
    ACTION = "ACTION"
    FACT = "FACT"


class Landmark(BaseModel):
    kind: str = LandmarkTypes.ACTION.value
    name: str


class Selection(BaseModel):
    name: str
    status: Optional[bool]
