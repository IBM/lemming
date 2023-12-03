from __future__ import annotations
from pydantic import BaseModel, model_validator
from typing import List, Optional, Any

from helpers.common_helper.hash_helper import get_list_hash


class Plan(BaseModel):
    actions: List[str] = []
    cost: int = 0
    plan_hash: Optional[str] = None

    @staticmethod
    def plan_to_text(plan: Plan) -> str:
        actions = ["(" + a + ")" for a in plan.actions]
        return (
            "\n".join(actions)
            + "\n"
            + "; cost = "
            f"{plan.cost} ({'unit cost' if plan.cost == 1 else 'general cost'})"
        )


class PlanningResult(BaseModel):
    plans: List[Plan]
    planner_name: Optional[str] = None
    planner_exit_code: Optional[int] = 0

    @model_validator(mode="before")
    @classmethod
    def custom_initializer(cls, data: Any) -> Any:
        if not data or "plans" not in data:
            return {"plans": []}

        return data

    @model_validator(mode="after")
    def set_plan_hashes(self) -> PlanningResult:
        for plan in self.plans:
            if not plan.plan_hash:
                plan.plan_hash = get_list_hash(plan.actions)

        return self
