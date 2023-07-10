from typing import List, Optional
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    Plan,
    SelectionInfo,
    PlanDisambiguatorOutput,
    SelectionPriority,
)
from helpers.graph_helper.graph_helper import get_dict_from_graph
from helpers.common_helper.exception_handler import planner_exception_handler
from helpers.plan_disambiguator_helper.plan_disambiguator_helper import (
    get_plan_disambiguator_output_filtered_by_selection_infos,
    get_choice_info_multiple_edges_without_landmark,
    append_landmarks_not_available_for_choice,
    set_nodes_with_multiple_edges,
    process_selection_priority,
    set_distance_to_terminal_nodes,
)
from helpers.graph_helper.graph_helper import (
    get_first_node_with_multiple_out_edges,
)


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
        (
            nodes_with_multiple_edges,
            nodes_traversed,
        ) = get_first_node_with_multiple_out_edges(g, True)
        choice_infos = append_landmarks_not_available_for_choice(
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
        )
        choice_infos = list(
            map(
                lambda choice_info: set_distance_to_terminal_nodes(
                    choice_info,
                    node_dist_from_initial_state,
                    node_dist_from_end_state,
                ),
                choice_infos,
            )
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
    choice_infos = list(
        map(
            lambda choice_info: set_distance_to_terminal_nodes(
                choice_info,
                node_dist_from_initial_state,
                node_dist_from_end_state,
            ),
            choice_infos,
        )
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
