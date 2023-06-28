from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Optional

from pydantic import BaseModel, Json


class NL2LTLRequest(BaseModel):
    domain_name: Optional[str]
    utterance: str


class LTLFormula(BaseModel):
    user_prompt: str
    formula_name: str
    formula_ltl: str
    formula_ppltl: str
    description: str
    confidence: float


class Declare(BaseModel):
    pattern: str
    symbols: List[str]


class CachedPrompt(BaseModel):
    utterance: str
    paraphrases: List[str]
    declare: List[Declare]


class LLMPrompt(BaseModel):
    prompt: str
    objects: List[str] = []
    actions: List[str] = []
    predicates: List[str] = []


def _build_llm_prompt_from_cached_prompt(data: Json[List[Dict]]) -> LLMPrompt:
    """Instantiate an LLM Prompt from parsed Cached prompt."""
    nl_prompts = [CachedPrompt.parse_obj(obj) for obj in data]
    body = ""
    for c_prompt in nl_prompts:
        for case in [c_prompt.utterance, *c_prompt.paraphrases]:
            for declare in c_prompt.declare:
                body += f"\nNL: {case}\n"
                body += f"PATTERN: {declare.pattern}\n"
                body += f"SYMBOLS: {', '.join(declare.symbols)}\n\n"
    return LLMPrompt(prompt=body)


def _parse_prompt_data(prompt_path: Path) -> LLMPrompt:
    """Parses a Cached prompt from a given path."""
    with open(prompt_path, "r") as f:
        data = json.load(f)
    prompt: LLMPrompt = _build_llm_prompt_from_cached_prompt(data)
    return prompt


def prompt_builder(prompt_path: Path) -> str:
    """Builds the LLM prompt given the path to a Cached prompt."""
    header = (
        "Translate natural language sentences into patterns.\n\n"
        "ALLOWED_PATTERN_NAMES: Existence, Absence,"
        "Response, ChainResponse, Precedence\n"
    )
    llm_prompt: LLMPrompt = _parse_prompt_data(prompt_path)
    return json.dumps({"prompt": header + llm_prompt.prompt})
