from typing import Dict, List, Optional
from pydantic import BaseModel

from planners.drivers.landmark_driver_datatype import Landmark


class SimulationResultUnit(BaseModel):
    chosen_edge: Optional[str]
    is_edge_selected: Optional[bool]
    num_remaining_plans: int
    is_from_landmark: Optional[bool]
    is_disambiguation_done: bool


class EdgeSelectionPayload(BaseModel):
    selected_edge: Optional[str]
    is_edge_selected: bool
    is_edge_from_landmark: bool
    plan_hashes: Optional[List[str]]


class EdgeSelectionUnit(BaseModel):
    edge: Optional[str]
    plan_hashes: Optional[List[str]]
    landmark: Optional[Landmark]

class EdgeChoiceUnit(BaseModel):
    edge_name_plan_hash_dict: Dict[str, List[str]]
    landmark: Optional[Landmark]