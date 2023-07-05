import random
from typing import Dict, List, Optional
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    Plan,
    SelectionInfo,
    PlanDisambiguatorOutput,
    SelectionPriority,
    ChoiceInfo,
)
from helpers.graph_helper.graph_helper import get_dict_from_graph
from helpers.common_helper.exception_handler import planner_exception_handler
from helpers.plan_disambiguator_helper.plan_disambiguator_helper import (
    get_plan_disambiguator_output_filtered_by_selection_infos,
    get_choice_info_multiple_edges_without_landmark,
    append_landmarks_not_available_for_choice,
    set_nodes_with_multiple_edges,
    get_min_dist_between_nodes_from_terminal_node,
)
from helpers.graph_helper.graph_helper import (
    get_first_node_with_multiple_out_edges,
)


def get_total_num_plans(choice_info: ChoiceInfo) -> int:
    return sum(
        [len(plans) for plans in choice_info.action_name_plan_hash_map.values()]
    )


def process_selection_priority(
    choice_infos_input: List[ChoiceInfo],
    selection_priority: SelectionPriority,
    edge_label_nodes_dict: Dict[str, List[str]],
    node_dist_from_initial_state: Dict[str, int],
    node_dist_from_end_state: Dict[str, int],
) -> List[ChoiceInfo]:
    choice_infos = list(
        map(
            lambda choice_info: choice_info.copy(deep=True),
            choice_infos_input,
        )
    )

    if (
        selection_priority == SelectionPriority.MAX_PLANS.value
        or selection_priority == SelectionPriority.MIN_PLANS.value
    ):
        choice_infos.sort(
            key=lambda choice_info: get_total_num_plans(choice_info),
            reverse=(selection_priority == SelectionPriority.MIN_PLANS.value),
        )
    elif selection_priority == SelectionPriority.RANDOM.value:
        random.shuffle(choice_infos)
    elif selection_priority == SelectionPriority.INIT_FORWARD.value:
        choice_infos.sort(
            key=lambda choice_info: get_min_dist_between_nodes_from_terminal_node(
                list(choice_info.action_name_plan_hash_map.keys()),
                edge_label_nodes_dict,
                node_dist_from_initial_state,
            )
        )
    elif selection_priority == SelectionPriority.GOAL_BACKWARD.value:
        choice_infos.sort(
            key=lambda choice_info: get_min_dist_between_nodes_from_terminal_node(
                list(choice_info.action_name_plan_hash_map.keys()),
                edge_label_nodes_dict,
                node_dist_from_end_state,
            )
        )

    return choice_infos


@planner_exception_handler
def get_selection_flow_output(
    selection_infos: Optional[List[SelectionInfo]],
    landmarks: List[Landmark],
    domain: str,
    problem: str,
    plans: List[Plan],
    selection_priority: SelectionPriority,
) -> PlanDisambiguatorOutput:
    (
        selected_plans,
        choice_infos,
        g,
        _,
        node_plan_hashes_dict,
        edge_plan_hash_dict,
        edge_label_nodes_dict,
        node_dist_from_initial_state,
        node_dist_from_end_state,
    ) = get_plan_disambiguator_output_filtered_by_selection_infos(
        selection_infos, landmarks, domain, problem, plans
    )
    networkx_graph = get_dict_from_graph(g)

    if (
        len(selected_plans) > 1
        and len(
            list(
                filter(
                    lambda choice_info: choice_info.is_available_for_choice,
                    choice_infos,
                )
            )
        )
        == 0
    ):  # manual selection
        nodes_with_multiple_edges = get_first_node_with_multiple_out_edges(
            g, True
        )
        return PlanDisambiguatorOutput(
            plans=selected_plans,
            choice_infos=append_landmarks_not_available_for_choice(
                landmarks,
                list(
                    map(
                        lambda payload: get_choice_info_multiple_edges_without_landmark(
                            node_with_multiple_edges=payload[0],
                            edges_traversed=payload[2],
                            plans=selected_plans,
                            is_forward=True,
                        ),
                        nodes_with_multiple_edges,
                    )
                ),
            ),
            networkx_graph=networkx_graph,
            node_plan_hashes_dict=node_plan_hashes_dict,
            edge_plan_hashes_dict={
                f"{label[0]}_{label[1]}": plan_hashes
                for label, plan_hashes in edge_plan_hash_dict.items()
            },
        )
    choice_infos = process_selection_priority(
        set_nodes_with_multiple_edges(
            append_landmarks_not_available_for_choice(landmarks, choice_infos),
            edge_label_nodes_dict,
        ),
        selection_priority,
        edge_label_nodes_dict,
        node_dist_from_initial_state,
        node_dist_from_end_state,
    )

    return PlanDisambiguatorOutput(
        plans=selected_plans,
        choice_infos=choice_infos,
        networkx_graph=networkx_graph,
        node_plan_hashes_dict=node_plan_hashes_dict,
        edge_plan_hashes_dict={
            f"{label[0]}_{label[1]}": plan_hashes
            for label, plan_hashes in edge_plan_hash_dict.items()
        },
    )
