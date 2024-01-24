from typing import Dict, List, Optional
from pydantic import BaseModel
from planners.drivers.landmark_driver_datatype import Landmark
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    PlanDisambiguationView,
    PlanningTask,
    LandmarkCategory,
)
from helpers.common_helper.file_helper import read_str_from_file


class PlannerInput(BaseModel):
    domain: str = ""
    problem: str = ""
    num_plans: int
    quality_bound: float
    timeout: Optional[int]
    case_sensitive: bool
    action_name_prefix_preserve: Optional[str]

    def set_domain_problem(self, domain_file_path: str, problem_file_path: str) -> None:
        self.domain = read_str_from_file(domain_file_path)
        self.problem = read_str_from_file(problem_file_path)

    def get_planning_task(self) -> PlanningTask:
        return PlanningTask(
            domain=self.domain,
            problem=self.problem,
            num_plans=self.num_plans,
            quality_bound=self.quality_bound,
            timeout=self.timeout,
            case_sensitive=self.case_sensitive,
            action_name_prefix_preserve=self.action_name_prefix_preserve
        )


class SimulationInput(BaseModel):
    plan_disambiguator_view: PlanDisambiguationView
    landmark_category: LandmarkCategory
    select_edge_randomly: bool
    use_landmark_to_select_edge: bool
    num_replicates: int
    setting_name: str
    planner_input: PlannerInput


class SimulationResultUnit(BaseModel):
    chosen_edge: Optional[str]
    is_edge_selected: Optional[bool]
    num_remaining_plans: int
    is_from_landmark: Optional[bool]
    is_disambiguation_done: bool
    landmark_category: LandmarkCategory


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
