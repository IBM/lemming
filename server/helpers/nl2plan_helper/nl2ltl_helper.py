from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from dacite import from_dict
from helpers.common_helper.hash_helper import get_list_hash
from helpers.planner_helper.planner_helper_data_types import Plan
from pydantic import BaseModel, validator
from pylogics.syntax.base import Formula
from watson_ai_planning.data_model.planning_types import PlanningResult


class NL2LTLRequest(BaseModel):
    utterance: str


class LTLFormula(BaseModel):
    formula_name: str
    formula_ltl: Formula
    formula_ppltl: Formula
    description: str
    confidence: float


class Prompt(BaseModel):
    example_translations: List[Translation]
    objects: List[str] = []
    actions: List[str] = []
    predicates: List[str] = []


class Translation(BaseModel):
    utterance: str
    paraphrases: List[str]
    declare: str


def prompt_builder():
    pass
