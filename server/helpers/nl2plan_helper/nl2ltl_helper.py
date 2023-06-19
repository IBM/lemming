from __future__ import annotations

from typing import List

from pydantic import BaseModel
from pylogics.syntax.base import Formula


class NL2LTLRequest(BaseModel):
    utterance: str


class LTLFormula(BaseModel):
    user_prompt = str
    formula_name = str
    formula_ltl = Formula
    formula_ppltl = Formula
    description = str
    confidence = float

    class Config:
        arbitrary_types_allowed = True


class Prompt(BaseModel):
    example_translations: List[Translation]
    objects: List[str] = []
    actions: List[str] = []
    predicates: List[str] = []


class Translation(BaseModel):
    utterance: str
    paraphrases: List[str]
    declare: str


def prompt_builder() -> str:
    return str()
