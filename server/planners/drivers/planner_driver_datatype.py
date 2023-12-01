from __future__ import annotations
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, model_validator
from typing import List, Optional

from helpers.common_helper.hash_helper import get_list_hash


@dataclass
class PlanDict:
    actions: List[str]
    cost: Optional[int]


@dataclass
class PlanningResultDict:
    plans: List[PlanDict]


class Plan(BaseModel):
    actions: List[str] = []
    cost: int = 0
    plan_hash: Optional[str] = None


class PlanningResult(BaseModel):
    plans: List[Plan]

    @model_validator(mode="after")
    def set_plan_hashes(self) -> PlanningResult:
        for plan in self.plans:
            if not plan.plan_hash:
                plan.plan_hash = get_list_hash(plan.actions)

        return self
