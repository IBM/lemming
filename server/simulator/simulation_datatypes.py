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
    landmark_category: LandmarkCategory = LandmarkCategory.RWH
    select_edge_randomly: bool = True
    use_landmark_to_select_edge: bool = False
    use_greedy_disjunctive_action_selection: bool = False
    num_replicates: int = 1
    setting_name: str = "test"
    planning_task: PlanningTask


class SimulationMetrics(BaseModel):
    num_edges_chosen: int
    num_landmarks_chosen: int
    is_disambiguation_done: bool


class SimulationResultUnit(BaseModel):
    chosen_edge: Optional[str]
    is_edge_selected: Optional[bool]
    num_remaining_plans: int
    is_from_landmark: Optional[bool]
    is_disambiguation_done: bool


class SimulationOutput(BaseModel):
    simulation_results: List[List[SimulationResultUnit]]
    simulation_input: SimulationInput

    def get_num_landmarks_from_chosen_edge(self, List[SimulationResultUnit]) -> int:
        return len(filter lambda edge: edge., self.chosen_edge)

    def get_simulation_metrics(self) -> List[SimulationMetrics]:
        return list(
            map(lambda simulation_result: SimulationMetrics(
            num_edges_chosen=(len(simulation_result.chosen_edge) -1 if simulation_result.chosen_edge is not None and len(simulation_result.chosen_edge) > 1 else 0),
            num_landmarks_chosen=0,
            is_disambiguation_done=False
        ), self.simulation_results)
        )
        

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
