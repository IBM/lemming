from pydantic.dataclasses import dataclass
from typing import List


@dataclass
class Landmark:
    facts: List[str]
    disjunctive: bool
    first_achievers: List[str]
