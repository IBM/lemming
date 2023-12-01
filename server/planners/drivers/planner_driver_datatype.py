from __future__ import annotations
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, model_validator
from typing import List, Optional, Any

from helpers.common_helper.hash_helper import get_list_hash


@dataclass
class PlanDict:
    actions: List[str]
    cost: Optional[int]


class Plan(BaseModel):
    actions: List[str] = []
    cost: int = 0
    plan_hash: Optional[str] = None


class PlanningResult(BaseModel):
    plans: List[Plan]
    planner_name: Optional[str] = None
    planner_exit_code: Optional[int] = 0

    @model_validator(mode="before")
    @classmethod
    def check_card_number_omitted(cls, data: Any) -> Any:
        if not data or "plans" not in data:
            return {"plans": []}

        return data

    @model_validator(mode="after")
    def set_plan_hashes(self) -> PlanningResult:
        for plan in self.plans:
            if not plan.plan_hash:
                plan.plan_hash = get_list_hash(plan.actions)

        return self
