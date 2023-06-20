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


class Translation(BaseModel):
    utterance: str
    paraphrases: List[str]
    symbols: List[str]
    declare: List[str]


class LLMPrompt(BaseModel):
    example_translations: List[Translation]
    objects: List[str] = []
    actions: List[str] = []
    predicates: List[str] = []


def _prompt_from_dict(data: Json[List[Dict]]) -> LLMPrompt:
    """Instantiate a Prompt from parsed data."""
    examples = []
    for obj in data:
        examples.append(
            Translation(
                utterance=obj["utterance"],
                paraphrases=obj["paraphrases"],
                symbols=obj["symbols"],
                declare=obj["declare"],
            )
        )
    return LLMPrompt(example_translations=examples)


def _parse_prompt_data(prompt_path: Path) -> LLMPrompt:
    """Parses a prompt from a given path."""
    with open(prompt_path, "r") as f:
        data = json.load(f)
    prompt: LLMPrompt = _prompt_from_dict(data)
    return prompt


def prompt_builder(prompt_path: Path) -> Json:
    """Builds a Json prompt from a given path."""
    header = (
        "Translate natural language sentences into patterns.\n\nALLOWED_PATTERN_NAMES: Existence, ExistenceTwo, "
        "Response, ChainResponse, RespondedExistence\n"
    )
    prompt: LLMPrompt = _parse_prompt_data(prompt_path)
    body = ""
    for example in prompt.example_translations:
        if len(example.declare) > 1:
            for pattern in example.declare:
                body += f"\nNL: {example.utterance}\n"
                body += f"PATTERN: {pattern}\n"
                body += f"SYMBOLS: {', '.join(example.symbols)}\n\n"
        else:
            body += f"\nNL: {example.utterance}\n"
            body += f"PATTERN: {example.declare[0]}\n"
            body += f"SYMBOLS: {', '.join(example.symbols)}\n\n"
    return json.dumps({"prompt": header + body})
