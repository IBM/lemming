import random
from typing import Dict, List, Optional, Tuple

from networkx import Graph
from helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topk,
)
from planners.drivers.planner_driver_datatype import PlanningResult
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    ChoiceInfo,
    PlanningTask,
    PlanDisambiguationView,
    PlanDisambiguatorInput,
    PlanDisambiguatorOutput,
    SelectionInfo,
    LandmarkCategory,
)
from helpers.plan_disambiguator_helper.selection_flow_helper import (
    get_selection_flow_output,
)
from helpers.plan_disambiguator_helper.build_flow_helper import (
    get_build_flow_output,
)
from simulator.simulation_datatypes import (
    SimulationResultUnit, EdgeSelectionPayload, EdgeSelectionUnit, EdgeChoiceUnit, SimulationInput, SimulationOutput)
from helpers.graph_helper.graph_helper import (
    get_edge_label,
)


def set_random_seed(seed: int) -> None:
    random.seed(seed)


def is_landmark_choice_info(choice_info: ChoiceInfo) -> bool:
    return choice_info.landmark is not None


def get_edges_from_choice_infos(
        choice_infos: List[ChoiceInfo],
        use_landmark: bool,
        is_landmark: bool = True) -> List[EdgeChoiceUnit]:
    action_names_landmarks: List[EdgeChoiceUnit] = []
    for choice_info in choice_infos:
        if use_landmark:
            if is_landmark_choice_info(choice_info) == is_landmark and len(choice_info.action_name_plan_hash_map) > 0:
                action_names_landmarks.append(
                    EdgeChoiceUnit(
                        edge_name_plan_hash_dict=choice_info.action_name_plan_hash_map,
                        landmark=choice_info.landmark
                    ))
        else:
            if len(choice_info.action_name_plan_hash_map) > 0:
                action_names_landmarks.append(
                    EdgeChoiceUnit(
                        edge_name_plan_hash_dict=choice_info.action_name_plan_hash_map,
                        landmark=choice_info.landmark
                    ))
    return action_names_landmarks


def choose_edge_landmark(edge_choice_units: List[EdgeChoiceUnit]) -> EdgeSelectionUnit:
    """
    returns chosen edge, plan hashes, and landmark
    """
    if len(edge_choice_units) >= 1:
        idx_0 = random.randint(0, len(edge_choice_units)-1)
        edges = list(edge_choice_units[idx_0].edge_name_plan_hash_dict.keys())
        idx_edge = random.randint(0, len(edges)-1)
        chosen_edge = edges[idx_edge]
        return EdgeSelectionUnit(
            edge=chosen_edge,
            plan_hashes=edge_choice_units[idx_0].edge_name_plan_hash_dict[chosen_edge],
            landmark=edge_choice_units[idx_0].landmark,
        )
    return EdgeSelectionUnit(
        edge=None,
        plan_hashes=None,
        landmark=None,
    )


def get_edge_landmark_from_plan_disambiguator_output(
        plan_disambiguator_output: PlanDisambiguatorOutput,
        use_landmark_to_select_edge: bool) -> EdgeSelectionUnit:
    if use_landmark_to_select_edge:
        edge_choice_units = get_edges_from_choice_infos(
            plan_disambiguator_output.choice_infos, use_landmark=True, is_landmark=True)
        edge_selection_unit = choose_edge_landmark(
            edge_choice_units)
        if edge_selection_unit.edge is None:  # edges not from landmarks
            edge_choice_units = get_edges_from_choice_infos(
                plan_disambiguator_output.choice_infos, use_landmark=True, is_landmark=False)
            edge_selection_unit = choose_edge_landmark(
                edge_choice_units)
        return edge_selection_unit

    edge_choice_units = get_edges_from_choice_infos(
        plan_disambiguator_output.choice_infos, use_landmark=False)
    return choose_edge_landmark(edge_choice_units)


def add_new_selection_to_plan_disambiguator_input(
        plan_disambiguator_input: PlanDisambiguatorInput,
        selected_edge: str,
        selected_plan_hashes: Optional[List[str]]) -> PlanDisambiguatorInput:
    selection_info = SelectionInfo(
        selected_first_achiever=selected_edge,
        selected_plan_hashes=selected_plan_hashes)
    new_plan_disambiguator_input = plan_disambiguator_input.model_copy(
        deep=True)
    new_plan_disambiguator_input.selection_infos.append(selection_info)
    return new_plan_disambiguator_input


def select_edge_among_choiceinfos(
        plan_disambiguator_output: PlanDisambiguatorOutput,
        use_landmark_to_select_edge: bool) -> EdgeSelectionPayload:
    edge_selection_unit = get_edge_landmark_from_plan_disambiguator_output(
        plan_disambiguator_output=plan_disambiguator_output,
        use_landmark_to_select_edge=use_landmark_to_select_edge)

    return EdgeSelectionPayload(
        selected_edge=edge_selection_unit.edge,
        is_edge_selected=(edge_selection_unit.edge is not None),
        is_edge_from_landmark=(edge_selection_unit.landmark is not None),
        plan_hashes=edge_selection_unit.plan_hashes
    )


def select_edge_random(
        edge_plan_hash_dict: Dict[Tuple[str, str], List[str]],
        g: Graph) -> EdgeSelectionPayload:
    edge, plan_hashes = random.choice(list(edge_plan_hash_dict.items()))

    return EdgeSelectionPayload(
        selected_edge=get_edge_label(g, edge),
        is_edge_selected=True,
        is_edge_from_landmark=False,
        plan_hashes=plan_hashes
    )


def select_edge(
        plan_disambiguator_output: PlanDisambiguatorOutput,
        edge_plan_hash_dict: Dict[Tuple[str, str], List[str]],
        g: Graph,
        select_edge_randomly: bool,
        use_landmark_to_select_edge: bool) -> EdgeSelectionPayload:
    """
    returns a plan_disambiguator input, a status to indicate if an edge is elected, a status to indicate if an edge is from landmark, and plan hashes
    """
    if len(plan_disambiguator_output.plans) <= 1:
        return EdgeSelectionPayload(
            selected_edge=None,
            is_edge_selected=False,
            is_edge_from_landmark=False,
            plan_hashes=None
        )
    return (select_edge_random(
        edge_plan_hash_dict=edge_plan_hash_dict, g=g) if select_edge_randomly else select_edge_among_choiceinfos(
        plan_disambiguator_output=plan_disambiguator_output,
        use_landmark_to_select_edge=use_landmark_to_select_edge))


def get_plan_disambuguator_output(
        plan_disambiguator_input: PlanDisambiguatorInput,
        plan_disambiguator_view: PlanDisambiguationView) -> Tuple[PlanDisambiguatorOutput, Dict[Tuple[str, str], List[str]], Graph]:
    if plan_disambiguator_view == PlanDisambiguationView.SELECT:  # select flow
        return get_selection_flow_output(
            selection_infos=plan_disambiguator_input.selection_infos,
            landmarks=plan_disambiguator_input.landmarks,
            domain=plan_disambiguator_input.domain,
            problem=plan_disambiguator_input.problem,
            plans=plan_disambiguator_input.plans,
            selection_priority=plan_disambiguator_input.selection_priority,
        )
    # build flow
    return get_build_flow_output(
        plan_disambiguator_input.selection_infos,
        plan_disambiguator_input.landmarks,
        plan_disambiguator_input.domain,
        plan_disambiguator_input.problem,
        plan_disambiguator_input.plans,
        (True if (plan_disambiguator_view ==
         PlanDisambiguationView.BUILD_FORWARD) else False),
    )


def simulate_view(
        planning_task: PlanningTask,
        planning_result: Optional[PlanningResult],
        landmarks: List[Landmark],
        plan_disambiguator_view: PlanDisambiguationView,
        num_replicates: int,
        select_edge_randomly: bool,
        use_landmark_to_select_edge: bool) -> List[List[SimulationResultUnit]]:
    plan_disambiguator_input = PlanDisambiguatorInput(
        selection_priority=None,
        selection_infos=[],
        landmarks=landmarks,
        plans=planning_result.plans,
        domain=planning_task.domain,
        problem=planning_task.problem
    )

    simulation_results: List[List[SimulationResultUnit]] = []

    for _ in range(num_replicates):
        plan_disambiguator_input_rep = plan_disambiguator_input.model_copy(
            deep=True)
        simulation_result_unit: List[SimulationResultUnit] = []
        plan_disambiguation_done = False
        while not plan_disambiguation_done:
            plan_disambiguator_output, edge_plan_hash_dict, g = get_plan_disambuguator_output(
                plan_disambiguator_input=plan_disambiguator_input_rep,
                plan_disambiguator_view=plan_disambiguator_view)

            if len(plan_disambiguator_output.plans) == 1:  # plan disambiguation completed
                simulation_result_unit.append(
                    SimulationResultUnit(
                        chosen_edge=None,
                        is_edge_selected=None,
                        num_remaining_plans=len(
                            plan_disambiguator_output.plans),
                        is_from_landmark=None,
                        is_disambiguation_done=True))
                plan_disambiguation_done = True
                continue

            edge_selection_payload = select_edge(
                plan_disambiguator_output=plan_disambiguator_output,
                edge_plan_hash_dict=edge_plan_hash_dict,
                g=g,
                select_edge_randomly=select_edge_randomly,
                use_landmark_to_select_edge=use_landmark_to_select_edge)

            if edge_selection_payload.is_edge_selected:
                plan_disambiguator_input_rep = add_new_selection_to_plan_disambiguator_input(
                    plan_disambiguator_input=plan_disambiguator_input_rep,
                    selected_edge=edge_selection_payload.selected_edge,
                    selected_plan_hashes=edge_selection_payload.plan_hashes
                )
                simulation_result_unit.append(
                    SimulationResultUnit(
                        chosen_edge=edge_selection_payload.selected_edge,
                        is_edge_selected=edge_selection_payload.is_edge_selected,
                        num_remaining_plans=len(
                            plan_disambiguator_output.plans),
                        is_from_landmark=edge_selection_payload.is_edge_from_landmark,
                        is_disambiguation_done=(
                            len(plan_disambiguator_output.plans) == 1)
                    )
                )
            else:
                simulation_result_unit.append(
                    SimulationResultUnit(
                        chosen_edge=None,
                        is_edge_selected=False,
                        num_remaining_plans=len(
                            plan_disambiguator_output.plans),
                        is_from_landmark=None,
                        is_disambiguation_done=False
                    )
                )
                plan_disambiguation_done = True
        simulation_results.append(simulation_result_unit)

    return simulation_results


def run_simulation(
        simulation_input: SimulationInput,
) -> SimulationOutput:
    planning_task = simulation_input.planner_input.get_planning_task()
    planning_result = get_plan_topk(planning_task)
    landmarks = get_landmarks_by_landmark_category(
        planning_task, simulation_input.landmark_category
    )
    return SimulationOutput(
        simulation_results=simulate_view(
            planning_task=planning_task,
            planning_result=planning_result,
            landmarks=landmarks,
            plan_disambiguator_view=simulation_input.plan_disambiguator_view,
            num_replicates=simulation_input.num_replicates,
            select_edge_randomly=simulation_input.select_edge_randomly,
            use_landmark_to_select_edge=simulation_input.use_landmark_to_select_edge),
        simulation_input=simulation_input.model_copy(deep=True))
