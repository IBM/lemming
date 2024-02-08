import random
import sys
from typing import Any, Dict, List, Optional, Tuple

from networkx import Graph
from server.helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topk,
)
from server.planners.drivers.planner_driver_datatype import PlanningResult
from server.helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    ChoiceInfo,
    PlanningTask,
    PlanDisambiguationView,
    PlanDisambiguatorInput,
    PlanDisambiguatorOutput,
    SelectionInfo,
)
from server.helpers.plan_disambiguator_helper.selection_flow_helper import (
    get_selection_flow_output,
)
from server.helpers.plan_disambiguator_helper.build_flow_helper import (
    get_build_flow_output,
)
from server.simulator.simulation_datatypes import (
    SimulationResultUnit,
    EdgeSelectionPayload,
    EdgeSelectionUnit,
    EdgeChoiceUnit,
    SimulationInput,
    SimulationOutput,
    SimulationMestricUnits,
    EdgeSelectionType,
)
from server.helpers.graph_helper.graph_helper import (
    get_edge_label,
)
from server.helpers.common_helper.file_helper import write_file_with_model_path


def set_random_seed(seed: int) -> None:
    random.seed(seed)


def is_landmark_choice_info(choice_info: ChoiceInfo) -> bool:
    return choice_info.landmark is not None


def get_edges_from_choice_infos(
    choice_infos: List[ChoiceInfo],
    use_landmark: bool,
    is_landmark: bool,
    use_greedy_disjunctive_action_selection: bool,
) -> List[EdgeChoiceUnit]:
    action_names_landmarks: List[EdgeChoiceUnit] = []
    for choice_info in choice_infos:
        if use_landmark:
            if (
                is_landmark_choice_info(choice_info) == is_landmark
                and len(choice_info.action_name_plan_hash_map) > 0
            ):
                if use_greedy_disjunctive_action_selection:
                    if choice_info.landmark.disjunctive:
                        action_names_landmarks.append(
                            EdgeChoiceUnit(
                                edge_name_plan_hash_dict=choice_info.action_name_plan_hash_map,
                                landmark=choice_info.landmark,
                            )
                        )
                else:
                    action_names_landmarks.append(
                        EdgeChoiceUnit(
                            edge_name_plan_hash_dict=choice_info.action_name_plan_hash_map,
                            landmark=choice_info.landmark,
                        )
                    )
        else:
            if len(choice_info.action_name_plan_hash_map) > 0:
                action_names_landmarks.append(
                    EdgeChoiceUnit(
                        edge_name_plan_hash_dict=choice_info.action_name_plan_hash_map,
                        landmark=choice_info.landmark,
                    )
                )
    return action_names_landmarks


def get_edge_with_min_plans(
    edge_choice_units: List[EdgeChoiceUnit],
) -> Optional[List[Tuple[Tuple[str, str], List[str], Landmark]]]:
    edges_with_minimum_num_plans: Optional[
        List[Tuple[Tuple[str, str], List[str], Landmark]]
    ] = None
    max_num_plan_hashes = sys.maxsize
    for edge_choice_unit in edge_choice_units:
        for (
            edge,
            plan_hashes,
        ) in edge_choice_unit.edge_name_plan_hash_dict.items():
            num_plan_hashes = len(plan_hashes)
            if num_plan_hashes > 0:
                if num_plan_hashes == max_num_plan_hashes:
                    edges_with_minimum_num_plans.append(
                        (edge, plan_hashes, edge_choice_unit.landmark)
                    )
                elif num_plan_hashes < max_num_plan_hashes:
                    edges_with_minimum_num_plans = [
                        (edge, plan_hashes, edge_choice_unit.landmark)
                    ]
                    max_num_plan_hashes = num_plan_hashes
    return edges_with_minimum_num_plans


def choose_edge_landmark(
    edge_choice_units: List[EdgeChoiceUnit],
    use_greedy_disjunctive_action_selection: bool,
) -> EdgeSelectionUnit:
    """
    returns chosen edge, plan hashes, and landmark
    """
    if (
        use_greedy_disjunctive_action_selection
    ):  # greedy edge selection with disjunctive action landmarks
        edges_with_landmarks_min_plans = get_edge_with_min_plans(
            edge_choice_units
        )
        if edges_with_landmarks_min_plans is not None:
            idx_0 = random.randint(0, len(edges_with_landmarks_min_plans) - 1)
            chosen_edge_choice_unit = edges_with_landmarks_min_plans[idx_0]
            return EdgeSelectionUnit(
                edge=chosen_edge_choice_unit[0],
                plan_hashes=chosen_edge_choice_unit[1],
                landmark=chosen_edge_choice_unit[2],
            )
        else:
            return EdgeSelectionUnit(
                edge=None,
                plan_hashes=None,
                landmark=None,
            )

    if len(edge_choice_units) >= 1:
        idx_0 = random.randint(0, len(edge_choice_units) - 1)
        edges = list(edge_choice_units[idx_0].edge_name_plan_hash_dict.keys())
        idx_edge = random.randint(0, len(edges) - 1)
        chosen_edge = edges[idx_edge]
        return EdgeSelectionUnit(
            edge=chosen_edge,
            plan_hashes=edge_choice_units[idx_0].edge_name_plan_hash_dict[
                chosen_edge
            ],
            landmark=edge_choice_units[idx_0].landmark,
        )

    return EdgeSelectionUnit(
        edge=None,
        plan_hashes=None,
        landmark=None,
    )


def get_edge_landmark_from_plan_disambiguator_output(
    plan_disambiguator_output: PlanDisambiguatorOutput,
    use_landmark_to_select_edge: bool,
    use_greedy_disjunctive_action_selection: bool,
) -> EdgeSelectionUnit:
    if use_landmark_to_select_edge:
        if use_greedy_disjunctive_action_selection:
            edge_choice_units = get_edges_from_choice_infos(
                plan_disambiguator_output.choice_infos,
                use_landmark=True,
                is_landmark=True,
                use_greedy_disjunctive_action_selection=use_greedy_disjunctive_action_selection,
            )
            edge_selection_unit = choose_edge_landmark(
                edge_choice_units=edge_choice_units,
                use_greedy_disjunctive_action_selection=use_greedy_disjunctive_action_selection,
            )
            if edge_selection_unit.edge is not None:
                return edge_selection_unit
        edge_choice_units = get_edges_from_choice_infos(
            plan_disambiguator_output.choice_infos,
            use_landmark=True,
            is_landmark=True,
            use_greedy_disjunctive_action_selection=False,
        )
        edge_selection_unit = choose_edge_landmark(
            edge_choice_units=edge_choice_units,
            use_greedy_disjunctive_action_selection=use_greedy_disjunctive_action_selection,
        )
        if edge_selection_unit.edge is None:  # edges not from landmarks
            edge_choice_units = get_edges_from_choice_infos(
                plan_disambiguator_output.choice_infos,
                use_landmark=True,
                is_landmark=False,
                use_greedy_disjunctive_action_selection=False,
            )
            edge_selection_unit = choose_edge_landmark(
                edge_choice_units=edge_choice_units,
                use_greedy_disjunctive_action_selection=use_greedy_disjunctive_action_selection,
            )
        return edge_selection_unit

    edge_choice_units = get_edges_from_choice_infos(
        plan_disambiguator_output.choice_infos,
        use_landmark=False,
        is_landmark=False,
        use_greedy_disjunctive_action_selection=False,
    )
    return choose_edge_landmark(
        edge_choice_units=edge_choice_units,
        use_greedy_disjunctive_action_selection=use_greedy_disjunctive_action_selection,
    )


def add_new_selection_to_plan_disambiguator_input(
    plan_disambiguator_input: PlanDisambiguatorInput,
    selected_edge: str,
    selected_plan_hashes: Optional[List[str]],
) -> PlanDisambiguatorInput:
    selection_info = SelectionInfo(
        selected_first_achiever=selected_edge,
        selected_plan_hashes=selected_plan_hashes,
    )
    new_plan_disambiguator_input = plan_disambiguator_input.model_copy(
        deep=True
    )
    new_plan_disambiguator_input.selection_infos.append(selection_info)
    return new_plan_disambiguator_input


def select_edge_among_choiceinfos(
    plan_disambiguator_output: PlanDisambiguatorOutput,
    use_landmark_to_select_edge: bool,
    use_greedy_disjunctive_action_selection: bool,
) -> EdgeSelectionPayload:
    edge_selection_unit = get_edge_landmark_from_plan_disambiguator_output(
        plan_disambiguator_output=plan_disambiguator_output,
        use_landmark_to_select_edge=use_landmark_to_select_edge,
        use_greedy_disjunctive_action_selection=use_greedy_disjunctive_action_selection,
    )

    return EdgeSelectionPayload(
        selected_edge=edge_selection_unit.edge,
        is_edge_selected=(edge_selection_unit.edge is not None),
        is_edge_from_landmark=(edge_selection_unit.landmark is not None),
        plan_hashes=edge_selection_unit.plan_hashes,
    )


def handle_edge(edge: Any) -> Tuple[str, str]:
    return tuple(edge.split("_")) if isinstance(edge, str) else edge


def select_edge_random_from_edge_plan_hash_dict(
    edge_plan_hash_dict: Dict[Tuple[str, str], List[str]], g: Graph
) -> EdgeSelectionPayload:
    edge, plan_hashes = random.choice(list(edge_plan_hash_dict.items()))

    return EdgeSelectionPayload(
        selected_edge=get_edge_label(g, handle_edge(edge)),
        is_edge_selected=True,
        is_edge_from_landmark=False,
        plan_hashes=plan_hashes,
    )


def get_all_actions_from_edge_plan_hash_dict(
    edge_plan_hash_dict: Dict[str, List[str]], g: Graph
) -> List[str]:
    return list(
        set(
            map(
                lambda edge: get_edge_label(g, handle_edge(edge)),
                edge_plan_hash_dict.keys(),
            )
        )
    )


def select_edge(
    plan_disambiguator_input: PlanDisambiguatorInput,
    plan_disambiguator_output: PlanDisambiguatorOutput,
    edge_plan_hash_dict: Dict[Tuple[str, str], List[str]],
    g: Graph,
    edge_selection_type: EdgeSelectionType,
) -> EdgeSelectionPayload:
    """
    returns a plan_disambiguator input, a status to indicate if an edge is elected,
    a status to indicate if an edge is from landmark, and plan hashes
    """

    if len(plan_disambiguator_output.plans) <= 1:
        return EdgeSelectionPayload(
            selected_edge=None,
            is_edge_selected=False,
            is_edge_from_landmark=False,
            plan_hashes=None,
        )

    if (
        (edge_selection_type == EdgeSelectionType.CHOICE_INFO)
        or (edge_selection_type == EdgeSelectionType.LANDMARK)
        or (edge_selection_type == EdgeSelectionType.LANDMARK_GREEDY)
        or (edge_selection_type == EdgeSelectionType.LANDMARK_CLOSEST_TO_GOAL)
        or (
            edge_selection_type == EdgeSelectionType.LANDMARK_CLOSEST_TO_INITIAL
        )
    ):
        return select_edge_among_choiceinfos(
            plan_disambiguator_output=plan_disambiguator_output,
            use_landmark_to_select_edge=(
                (edge_selection_type == EdgeSelectionType.LANDMARK)
                or (edge_selection_type == EdgeSelectionType.LANDMARK_GREEDY)
            ),
            use_greedy_disjunctive_action_selection=(
                edge_selection_type == EdgeSelectionType.LANDMARK_GREEDY
            ),
        )

    if (edge_selection_type == EdgeSelectionType.FREQUENCY_ACTION_MOST) or (
        edge_selection_type == EdgeSelectionType.FREQUENCY_ACTION_LEAST
    ):
        pass

    if edge_selection_type == EdgeSelectionType.RANDOM:
        return select_edge_random_from_edge_plan_hash_dict(
            edge_plan_hash_dict=edge_plan_hash_dict, g=g
        )

    return EdgeSelectionPayload()


def get_plan_disambuguator_output(
    plan_disambiguator_input: PlanDisambiguatorInput,
    plan_disambiguator_view: PlanDisambiguationView,
) -> Tuple[PlanDisambiguatorOutput, Dict[Tuple[str, str], List[str]], Graph]:
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
        (
            True
            if (plan_disambiguator_view == PlanDisambiguationView.BUILD_FORWARD)
            else False
        ),
    )


def simulate_view(
    planning_task: PlanningTask,
    planning_result: Optional[PlanningResult],
    landmarks: List[Landmark],
    plan_disambiguator_view: PlanDisambiguationView,
    num_replicates: int,
    edge_selection_type: EdgeSelectionType,
) -> List[List[SimulationResultUnit]]:
    plan_disambiguator_input = PlanDisambiguatorInput(
        selection_priority=None,
        selection_infos=[],
        landmarks=landmarks,
        plans=planning_result.plans,
        domain=planning_task.domain,
        problem=planning_task.problem,
    )

    simulation_results: List[List[SimulationResultUnit]] = []

    for _ in range(num_replicates):
        plan_disambiguator_input_rep = plan_disambiguator_input.model_copy(
            deep=True
        )
        simulation_result_unit: List[SimulationResultUnit] = []
        plan_disambiguation_done = False
        while not plan_disambiguation_done:
            (
                plan_disambiguator_output,
                edge_plan_hash_dict,
                g,
            ) = get_plan_disambuguator_output(
                plan_disambiguator_input=plan_disambiguator_input_rep,
                plan_disambiguator_view=plan_disambiguator_view,
            )

            if (
                len(plan_disambiguator_output.plans) == 1
            ):  # plan disambiguation completed
                simulation_result_unit.append(
                    SimulationResultUnit(
                        chosen_edge=None,
                        is_edge_selected=None,
                        num_remaining_plans=len(
                            plan_disambiguator_output.plans
                        ),
                        is_from_landmark=None,
                        is_disambiguation_done=True,
                        num_choice_infos=len(
                            plan_disambiguator_output.choice_infos
                        ),
                        num_nodes=len(
                            plan_disambiguator_output.node_plan_hashes_dict
                        ),
                        num_edges=len(
                            plan_disambiguator_output.edge_plan_hashes_dict
                        ),
                        num_actions=len(
                            get_all_actions_from_edge_plan_hash_dict(
                                edge_plan_hash_dict=plan_disambiguator_output.edge_plan_hashes_dict,
                                g=g,
                            )
                        ),
                        plan_costs=plan_disambiguator_output.get_plan_costs(),
                    )
                )
                plan_disambiguation_done = True
                continue

            edge_selection_payload = select_edge(
                plan_disambiguator_input=plan_disambiguator_input_rep,
                plan_disambiguator_output=plan_disambiguator_output,
                edge_plan_hash_dict=edge_plan_hash_dict,
                g=g,
                edge_selection_type=edge_selection_type,
            )

            if edge_selection_payload.is_edge_selected:
                plan_disambiguator_input_rep = (
                    add_new_selection_to_plan_disambiguator_input(
                        plan_disambiguator_input=plan_disambiguator_input_rep,
                        selected_edge=edge_selection_payload.selected_edge,
                        selected_plan_hashes=edge_selection_payload.plan_hashes,
                    )
                )
                simulation_result_unit.append(
                    SimulationResultUnit(
                        chosen_edge=edge_selection_payload.selected_edge,
                        is_edge_selected=edge_selection_payload.is_edge_selected,
                        num_remaining_plans=len(
                            plan_disambiguator_output.plans
                        ),
                        is_from_landmark=edge_selection_payload.is_edge_from_landmark,
                        is_disambiguation_done=(
                            len(plan_disambiguator_output.plans) == 1
                        ),
                        num_choice_infos=len(
                            plan_disambiguator_output.choice_infos
                        ),
                        num_nodes=len(
                            plan_disambiguator_output.node_plan_hashes_dict
                        ),
                        num_edges=len(
                            plan_disambiguator_output.edge_plan_hashes_dict
                        ),
                        num_actions=len(
                            get_all_actions_from_edge_plan_hash_dict(
                                edge_plan_hash_dict=plan_disambiguator_output.edge_plan_hashes_dict,
                                g=g,
                            )
                        ),
                        plan_costs=plan_disambiguator_output.get_plan_costs(),
                    )
                )
            else:
                simulation_result_unit.append(
                    SimulationResultUnit(
                        chosen_edge=None,
                        is_edge_selected=False,
                        num_remaining_plans=len(
                            plan_disambiguator_output.plans
                        ),
                        is_from_landmark=None,
                        is_disambiguation_done=False,
                        num_choice_infos=len(
                            plan_disambiguator_output.choice_infos
                        ),
                        num_nodes=len(
                            plan_disambiguator_output.node_plan_hashes_dict
                        ),
                        num_edges=len(
                            plan_disambiguator_output.edge_plan_hashes_dict
                        ),
                        num_actions=len(
                            get_all_actions_from_edge_plan_hash_dict(
                                edge_plan_hash_dict=plan_disambiguator_output.edge_plan_hashes_dict,
                                g=g,
                            )
                        ),
                        plan_costs=plan_disambiguator_output.get_plan_costs(),
                    )
                )
                plan_disambiguation_done = True
        simulation_results.append(simulation_result_unit)

    return simulation_results


def run_simulation(
    simulation_input: SimulationInput,
) -> SimulationOutput:
    planning_result = get_plan_topk(simulation_input.planning_task)
    landmarks = get_landmarks_by_landmark_category(
        simulation_input.planning_task, simulation_input.landmark_category.value
    )
    return SimulationOutput(
        simulation_results=simulate_view(
            planning_task=simulation_input.planning_task,
            planning_result=planning_result,
            landmarks=landmarks,
            plan_disambiguator_view=simulation_input.plan_disambiguator_view,
            num_replicates=simulation_input.num_replicates,
            edge_selection_type=simulation_input.edge_selection_type,
        ),
        simulation_input=simulation_input.model_copy(deep=True),
    )


def run_simulation_unit(simulation_input: SimulationInput) -> Tuple[str, str]:
    simulation_output = run_simulation(simulation_input)
    metrics = simulation_output.get_simulation_metrics()
    raw_output_file_path = write_file_with_model_path(
        file_name=simulation_input.get_name() + "_raw_output",
        file_path=simulation_input.folder_path,
        file_extension="txt",
        model=simulation_output,
    )
    metrics_file_path = write_file_with_model_path(
        file_name=simulation_input.get_name() + "_metrics",
        file_path=simulation_input.folder_path,
        file_extension="txt",
        model=SimulationMestricUnits(simulation_metrics_units=metrics),
    )
    return raw_output_file_path, metrics_file_path
