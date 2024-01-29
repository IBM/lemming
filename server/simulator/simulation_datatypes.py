from typing import Dict, List, Optional
from pydantic import BaseModel
from planners.drivers.landmark_driver_datatype import Landmark
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    PlanDisambiguationView,
    PlanningTask,
    LandmarkCategory,
)


class SimulationInput(BaseModel):
    plan_disambiguator_view: PlanDisambiguationView
    landmark_category: LandmarkCategory
    select_edge_randomly: bool
    use_landmark_to_select_edge: bool
    num_replicates: int
    setting_name: str
    planning_task: PlanningTask


class SimulationResultUnit(BaseModel):
    chosen_edge: Optional[str]
    is_edge_selected: Optional[bool]
    num_remaining_plans: int
    is_from_landmark: Optional[bool]
    is_disambiguation_done: bool


class SimulationOutput(BaseModel):
    simulation_results: List[List[SimulationResultUnit]]
    simulation_input: SimulationInput


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
