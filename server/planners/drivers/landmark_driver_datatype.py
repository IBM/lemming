from __future__ import annotations
from pydantic import BaseModel, model_validator
from typing import List


class Landmark(BaseModel):
    facts: List[str]
    disjunctive: bool
    first_achievers: List[str]

    @model_validator(mode="after")
    def strip_landmark_strings(self) -> Landmark:
        new_landmark_object = self
        new_landmark_object.first_achievers = [
            fa.strip() for fa in self.first_achievers
        ]

        return new_landmark_object
