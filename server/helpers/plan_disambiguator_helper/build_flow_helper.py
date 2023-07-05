from typing import Any, List, Optional, Set
from helpers.common_helper.exception_handler import planner_exception_handler
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    SelelctionInfo,
    Plan,
    PlanDisambiguatorOutput,
    ChoiceInfo,
)
from helpers.plan_disambiguator_helper.plan_disambiguator_helper import (
    get_choice_info_multiple_edges_without_landmark,
    get_plan_disambiguator_output_filtered_by_selection_infos,
    sort_choice_info_by_distance_to_terminal_nodes,
    set_distance_to_terminal_nodes,
)
from helpers.graph_helper.graph_helper import (
    get_first_node_with_multiple_out_edges,
    get_dict_from_graph,
    get_graph_upto_nodes,
)


@planner_exception_handler
def get_build_flow_output(
    selection_infos: Optional[List[SelelctionInfo]],
    landmarks: List[Landmark],
    domain: str,
    problem: str,
    plans: List[Plan],
    is_forward: bool,
) -> PlanDisambiguatorOutput:
    (
        selected_plans,
        _,
        g,
        _,
        node_plan_hashes_dict,
        edge_plan_hash_dict,
        _,
        node_dist_from_initial_state,
        node_dist_from_end_state,
    ) = get_plan_disambiguator_output_filtered_by_selection_infos(
        selection_infos, landmarks, domain, problem, plans
    )
    networkx_graph = get_dict_from_graph(g)
    if len(selected_plans) <= 1:  # no plans to disambiguate
        return PlanDisambiguatorOutput(
            plans=selected_plans,
            choice_infos=[],
            networkx_graph=networkx_graph,
            node_plan_hashes_dict=node_plan_hashes_dict,
            edge_plan_hashes_dict={
                f"{label[0]}_{label[1]}": plan_hashes
                for label, plan_hashes in edge_plan_hash_dict.items()
            },
        )

    (
        node_search_results,
        nodes_traversed,
    ) = get_first_node_with_multiple_out_edges(g, is_forward)

    if len(node_search_results) == 0:  # no selection needed
        return PlanDisambiguatorOutput(
            plans=selected_plans,
            choice_infos=[],
            networkx_graph=networkx_graph,
            node_plan_hashes_dict=node_plan_hashes_dict,
            edge_plan_hashes_dict={
                f"{label[0]}_{label[1]}": plan_hashes
                for label, plan_hashes in edge_plan_hash_dict.items()
            },
        )

    edges_to_traverse_to_remove_from_graph: Set[Any] = set()
    new_choice_infos: List[ChoiceInfo] = list()
    for (
        node_with_multiple_out_edges,
        out_edges_first_node_with_multiple_out_edges,
        edges_traversed,
    ) in node_search_results:
        new_choice_infos.append(
            get_choice_info_multiple_edges_without_landmark(
                node_with_multiple_edges=node_with_multiple_out_edges,
                edges_traversed=edges_traversed,
                plans=selected_plans,
                is_forward=is_forward,
            )
        )
        for edge in out_edges_first_node_with_multiple_out_edges:
            edges_to_traverse_to_remove_from_graph.add(edge)

    nodes_to_end = set(
        map(
            lambda edge: edge[1 if is_forward else 0],
            out_edges_first_node_with_multiple_out_edges,
        )
    )
    networkx_graph = get_dict_from_graph(
        get_graph_upto_nodes(g, nodes_to_end, nodes_traversed, is_forward)
    )
    new_choice_infos = set_distance_to_terminal_nodes(
        sort_choice_info_by_distance_to_terminal_nodes(
            new_choice_infos,
            node_dist_from_initial_state
            if is_forward
            else node_dist_from_end_state,
        ),
        node_dist_from_initial_state,
        node_dist_from_end_state,
    )
    return PlanDisambiguatorOutput(
        plans=selected_plans,
        choice_infos=new_choice_infos,
        networkx_graph=networkx_graph,
        first_achiever_edge_dict={},
        node_plan_hashes_dict=node_plan_hashes_dict,
        edge_plan_hashes_dict={
            f"{label[0]}_{label[1]}": plan_hashes
            for label, plan_hashes in edge_plan_hash_dict.items()
        },
    )
