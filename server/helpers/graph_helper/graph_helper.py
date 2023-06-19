from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple

import pydot
from helpers.common_helper.data_type_helper import merge_sets
from helpers.planner_helper.planner_helper_data_types import Plan
from networkx import Graph, nx_pydot, set_node_attributes
from networkx.readwrite import json_graph


def convert_dot_str_to_networkx_graph(dot_str: str) -> Graph:
    graphs = pydot.graph_from_dot_data(dot_str)  # convert to Pydot Objects
    return nx_pydot.from_pydot(graphs[0])


def get_dict_from_graph(g: Graph) -> Any:
    return json_graph.node_link_data(g)


def get_root_node_in_digraph(g: Graph) -> Optional[Any]:
    if len(g.nodes) == 0:
        return None
    root = [n for n, d in g.in_degree() if d == 0]
    return root[0]


def get_end_goal_node_in_digraph(g: Graph) -> Optional[Any]:
    if len(g.nodes) == 0:
        return None
    end_goal = [n for n, d in g.out_degree() if d == 0]
    return end_goal[0]


def get_edge_label(g: Graph, edge: Any) -> Optional[str]:
    if len(g.nodes) == 0:
        return None
    edge_data = g.get_edge_data(edge[0], edge[1])
    edge_label: str = edge_data[0]["label"].replace('"', "")
    return edge_label


def get_first_node_with_multiple_out_edges(
    g: Graph,
    first_achiever_plan_idx_dict: Dict[Any, List[Any]],
    is_forward: bool = True,
) -> Optional[Tuple[Any, Optional[Any], List[Any], List[Any]]]:
    """
    returns 1) node with multiple out edges, 2) first achiever in the node, 3) out edges from the node, and 4) edges traversed up to the node
    """
    if len(g.nodes) == 0:
        return None
    root: Optional[Any] = None
    # find a node to start
    root = (
        get_root_node_in_digraph(g)
        if is_forward
        else get_end_goal_node_in_digraph(g)
    )
    queue: List[Any] = list()
    queue.append(root)
    edges_traversed: List[Any] = list()
    while len(queue) > 0:
        new_queue: List[Any] = list()
        for node in queue:
            edges = (
                list(g.out_edges(node))
                if is_forward
                else list(g.in_edges(node))
            )
            for edge in edges:
                edge_label = get_edge_label(g, edge)

                if (
                    len(edges) > 1
                    and edge_label in first_achiever_plan_idx_dict
                ):
                    return (
                        deepcopy(node),
                        edge_label,
                        edges,
                        edges_traversed,
                    )

                if len(edges) == 1:
                    edges_traversed.append(edge_label)

                if is_forward:
                    new_queue.append(edge[1])
                else:
                    new_queue.append(edge[0])

            if len(edges) > 1:  # out edges are not first achievers
                return deepcopy(node), None, edges, edges_traversed

        queue = new_queue
    return None


def get_all_nodes_coming_from_node(
    g: Graph,
    source_node: Any,
    nodes_to_exclude: Set[Any] = set(),
    is_forward: bool = True,
) -> Set[Any]:
    if len(g.nodes) == 0:
        return set()
    nodes: Set[Any] = set()
    queue: List[Any] = list()
    queue.append(source_node)
    while len(queue) > 0:
        new_queue: List[Any] = list()
        for node in queue:
            edges = (
                list(g.out_edges(node))
                if is_forward
                else list(g.in_edges(node))
            )
            for edge in edges:
                target_node = edge[1] if is_forward else edge[0]
                if (
                    target_node not in nodes
                    and target_node not in nodes_to_exclude
                ):
                    nodes.add(target_node)
                    new_queue.append(target_node)
        queue = new_queue
    return nodes


def get_nodes_to_exclude(
    g: Graph, nodes_to_start: Set[Any], is_forward: bool
) -> Set[Any]:
    if len(g.nodes) == 0:
        return set()
    nodes_to_remove: List[Set[Any]] = list()
    for node_start in nodes_to_start:
        nodes_to_remove.append(
            get_all_nodes_coming_from_node(g, node_start, set(), is_forward)
        )

    merger: Set[Any] = merge_sets(nodes_to_remove)
    return merger


def remove_nodes_from_graph(g: Graph, nodes_to_remove: Set[Any]) -> Graph:
    new_graph = g.copy()
    if len(g.nodes) == 0:
        return new_graph
    new_graph.remove_nodes_from(list(nodes_to_remove))
    return new_graph


def get_graph_upto_nodes(
    g: Graph, nodes_to_end: Set[Any], is_forward: bool
) -> Graph:
    if len(g.nodes) == 0:
        return g.copy()
    nodes_to_exclude = get_nodes_to_exclude(g, nodes_to_end, is_forward)
    return remove_nodes_from_graph(g, nodes_to_exclude)


def get_node_name_plan_hash_list(
    g: Graph, plans: List[Plan], is_forward: bool
) -> Dict[str, List[str]]:
    """
    returns a dictionary of node names (keys) and lists of plan hashes
    """
    if len(g.nodes) == 0:
        return dict()

    start_node = (
        get_root_node_in_digraph(g)
        if is_forward
        else get_end_goal_node_in_digraph(g)
    )
    node_list_plan_hash_dict: Dict[str, List[str]] = dict()
    queue: List[Any] = list()
    queue.append(start_node)
    depth = 0
    while len(queue) > 0:
        new_queue: List[Any] = list()
        for node in queue:
            edges = (
                list(g.out_edges(node))
                if is_forward
                else list(g.in_edges(node))
            )
            plan_hashes_for_node: Set[str] = set()
            for edge in edges:
                edge_label = get_edge_label(g, edge)
                for plan in plans:
                    if depth < len(plan.actions):
                        if edge_label in plan.actions[depth]:
                            plan_hashes_for_node.add(plan.plan_hash[:])
                target_node = edge[1] if is_forward else edge[0]
                new_queue.append(target_node)
            node_list_plan_hash_dict[node] = list(plan_hashes_for_node)
        depth += 1
        queue = new_queue
    return node_list_plan_hash_dict


def get_graph_with_number_of_plans_label(
    g: Graph, node_list_plan_hash_dict: Dict[str, List[str]]
) -> Graph:
    """
    returns a deep copy of a graph with "num_plans" attribute
    """
    graph_with_new_attributes = g.copy()
    if len(g.nodes) == 0:
        return graph_with_new_attributes
    attributes: Dict[str, Dict[str, int]] = {
        node: {"num_plans": len(plan_hashes)}
        for node, plan_hashes in node_list_plan_hash_dict.items()
    }
    set_node_attributes(graph_with_new_attributes, attributes)
    return graph_with_new_attributes
