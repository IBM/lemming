from typing import List, Optional

from helpers.common_helper.exception_handler import planner_exception_handler
from helpers.graph_helper.graph_helper import (
  get_dict_from_graph, get_first_node_with_multiple_out_edges,
  get_graph_upto_nodes)
from helpers.plan_disambiguator_helper.plan_disambiguator_helper import (
  filter_in_choice_info_by_first_achiever,
  get_choice_info_multiple_edges_without_landmark,
  get_first_achiever_out_edge_dict, get_merged_first_achievers_dict,
  get_plan_disambiguator_output_filtered_by_selection_infos)
from helpers.planner_helper.planner_helper_data_types import (
  Landmark, Plan, PlanDisambiguatorOutput, SelelctionInfo)


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
        choice_infos,
        g,
        _,
        node_plan_hashes_dict,
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
        )

    first_achiever_plan_idx_dict = get_merged_first_achievers_dict(choice_infos)
    node_search_result = get_first_node_with_multiple_out_edges(
        g, first_achiever_plan_idx_dict, is_forward
    )

    if node_search_result is None:  # no selection needed
        return PlanDisambiguatorOutput(
            plans=selected_plans,
            choice_infos=[],
            networkx_graph=networkx_graph,
            node_plan_hashes_dict=node_plan_hashes_dict,
        )

    (
        node_with_multiple_out_edges,
        first_achiever,
        out_edges_first_node_with_multiple_out_edges,
        edges_traversed,
    ) = node_search_result

    # get a graph to render

    nodes_to_end = set(
        map(
            lambda edge: edge[1 if is_forward else 0],
            out_edges_first_node_with_multiple_out_edges,
        )
    )
    networkx_graph = get_dict_from_graph(
        get_graph_upto_nodes(g, nodes_to_end, is_forward)
    )

    if first_achiever is None:  # a node with multiple edges, no first achiever
        return PlanDisambiguatorOutput(
            plans=selected_plans,
            choice_infos=[
                get_choice_info_multiple_edges_without_landmark(
                    node_with_multiple_edges=node_with_multiple_out_edges,
                    edges_traversed=edges_traversed,
                    plans=selected_plans,
                    is_forward=is_forward,
                )
            ],
            networkx_graph=networkx_graph,
            node_plan_hashes_dict=node_plan_hashes_dict,
        )

    # first achiever for disambiguating plan is found
    turn_choice_infos = filter_in_choice_info_by_first_achiever(
        choice_infos, first_achiever
    )
    first_achiever_edge_dict = get_first_achiever_out_edge_dict(
        edges_traversed, selected_plans, turn_choice_infos[0], is_forward
    )
    return PlanDisambiguatorOutput(
        plans=selected_plans,
        choice_infos=turn_choice_infos,
        networkx_graph=networkx_graph,
        first_achiever_edge_dict=first_achiever_edge_dict,
        node_plan_hashes_dict=node_plan_hashes_dict,
    )
