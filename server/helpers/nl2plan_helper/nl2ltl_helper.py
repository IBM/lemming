from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict

from pydantic import BaseModel, Json
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
    symbols: List[str]
    declare: List[str]


def _prompt_from_dict(data: Json[List[Dict]]) -> Prompt:
    """Instantiate a Prompt from parsed data."""
    prompt = Prompt()
    for obj in data:
        prompt.example_translations.append(
            Translation(
                utterance=obj["utterance"],
                paraphrases=obj["paraphrases"],
                declare=obj["declare"],
            )
        )
    return prompt


def _parse_prompt_data(prompt_path: Path) -> Prompt:
    """Parses a prompt from a given path."""
    with open(prompt_path, "r") as f:
        data = json.load(f)
    prompt: Prompt = _prompt_from_dict(data)
    return prompt


def prompt_builder(prompt_path: Path) -> str:
    """Builds a prompt from a given path."""
    header = (
        "Translate natural language sentences into patterns.\n\nALLOWED_PATTERN_NAMES: Existence, ExistenceTwo, "
        "Response, ChainResponse, RespondedExistence\n"
    )
    prompt: Prompt = _parse_prompt_data(prompt_path)
    body = ""
    for example in prompt.example_translations:
        if len(example.declare) > 1:
            for pattern in example.declare:
                body += f"\nNL: {example.utterance}\n"
                body += f"PATTERN: {pattern}\n"
                body += f"SYMBOLS: {', '.join(example.symbols)}\n\n"
        body += f"\nNL: {example.utterance}\n"
        body += f"PATTERN: {example.declare[0]}\n"
        body += f"SYMBOLS: {', '.join(example.symbols)}\n\n"
    return header + body
