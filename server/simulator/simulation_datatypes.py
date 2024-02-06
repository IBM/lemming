from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel
from planners.drivers.landmark_driver_datatype import Landmark
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    PlanDisambiguationView,
    PlanningTask,
    LandmarkCategory,
)


class EdgeSelectionType(str, Enum):
    RANDOM = "random"
    CHOICE_INFO = "choice_info"
    FREQUENCY_MOST = "frequency_most"
    FREQUENCY_LEAST = "frequency_least"
    LANDMARK = "landmark"
    LANDMARK_GREEDY = "landmark_greedy"
    DISTANCE_INITIAL = "distance_initial"
    DISTANCE_GOAL = "distance_goal"


class SimulationInput(BaseModel):
    plan_disambiguator_view: PlanDisambiguationView = PlanDisambiguationView.SELECT
    landmark_category: LandmarkCategory = LandmarkCategory.RWH
    edge_selection_type: EdgeSelectionType = EdgeSelectionType.RANDOM
    num_replicates: int = 1
    setting_name: str = "test"
    folder_path: str = ""
    planning_task: PlanningTask

    def get_name(self) -> str:
        lst = [self.setting_name,
               self.plan_disambiguator_view.value,
               self.landmark_category.value,
               self.edge_selection_type.value]
        return "_".join(lst)


class SimulationMetrics(BaseModel):
    num_edges_chosen: int
    num_landmarks_chosen: int
    is_disambiguation_done: bool


class SimulationMestricUnits(BaseModel):
    simulation_metrics_units: List[SimulationMetrics]


class SimulationResultUnit(BaseModel):
    chosen_edge: Optional[str]
    is_edge_selected: Optional[bool]
    num_remaining_plans: int
    is_from_landmark: Optional[bool]
    is_disambiguation_done: bool
    num_choice_infos: Optional[int] = None
    num_nodes: Optional[int] = None
    num_edges: Optional[int] = None
    num_actions: Optional[int] = None
    plan_costs: Optional[List[int]] = None


class SimulationOutput(BaseModel):
    simulation_results: List[List[SimulationResultUnit]]
    simulation_input: SimulationInput

    def get_num_edges_chosen(self, simulation_result_units: List[SimulationResultUnit]) -> int:
        if len(simulation_result_units) == 0:
            return 0
        if simulation_result_units[-1].is_disambiguation_done:
            return (len(simulation_result_units) - 1)
        return len(simulation_result_units)

    def get_num_landmarks(self, simulation_result_units: List[SimulationResultUnit]) -> int:
        return len(
            list(filter(
                lambda simulation_result_unit: (
                    simulation_result_unit.is_from_landmark is not None and simulation_result_unit.is_from_landmark), simulation_result_units)))

    def get_simulation_metrics(self) -> List[SimulationMetrics]:
        return list(
            map(lambda simulation_result_units: SimulationMetrics(
                num_edges_chosen=self.get_num_edges_chosen(
                    simulation_result_units),
                num_landmarks_chosen=self.get_num_landmarks(
                    simulation_result_units),
                is_disambiguation_done=simulation_result_units[-1].is_disambiguation_done if len(
                    simulation_result_units) > 0 else False
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
