from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict

from pydantic import BaseModel, Json


class NL2LTLRequest(BaseModel):
    utterance: str


class LTLFormula(BaseModel):
    user_prompt: str
    formula_name: str
    formula_ltl: str
    formula_ppltl: str
    description: str
    confidence: float


class Translation(BaseModel):
    utterance: str
    paraphrases: List[str]
    declare: str
    symbols: List[str]


class LLMPrompt(BaseModel):
    example_translations: List[Translation]
    objects: List[str] = []
    actions: List[str] = []
    predicates: List[str] = []


def _prompt_from_dict(data: Json[List[Dict]]) -> LLMPrompt:
    """Instantiate a Prompt from parsed data."""
    examples = []
    for obj in data:
        utterance = obj["utterance"]
        paraphrases = obj["paraphrases"]
        for pattern_obj in obj["declare"]:
            examples.append(
                Translation(
                    utterance=utterance,
                    paraphrases=paraphrases,
                    declare=pattern_obj["pattern"],
                    symbols=pattern_obj["symbols"],
                )
            )
    return LLMPrompt(example_translations=examples)


def _parse_prompt_data(prompt_path: Path) -> LLMPrompt:
    """Parses a prompt from a given path."""
    with open(prompt_path, "r") as f:
        data = json.load(f)
    prompt: LLMPrompt = _prompt_from_dict(data)
    return prompt


def prompt_builder(prompt_path: Path) -> str:
    """Builds a Json prompt from a given path."""
    header = (
        "Translate natural language sentences into patterns.\n\nALLOWED_PATTERN_NAMES: Existence, Absence,"
        "Response, ChainResponse, RespondedExistence, Precedence\n"
    )
    prompt: LLMPrompt = _parse_prompt_data(prompt_path)
    body = ""
    for example in prompt.example_translations:
        body += f"\nNL: {example.utterance}\n"
        body += f"PATTERN: {example.declare}\n"
        body += f"SYMBOLS: {', '.join(example.symbols)}\n\n"
    return json.dumps({"prompt": header + body})
