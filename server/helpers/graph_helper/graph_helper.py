from copy import deepcopy
import re
from typing import Any, Dict, List, Optional, Set, Tuple
import pydot
from networkx import Graph, nx_pydot, set_node_attributes
from networkx.readwrite import json_graph
from helpers.common_helper.data_type_helper import merge_sets
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    Plan,
    ChoiceInfo,
)


def edit_edge_labels(g: Graph) -> Graph:
    new_graph = g.copy()
    for edge in new_graph.edges:
        edge_data = new_graph.get_edge_data(edge[0], edge[1])
        if (
            edge_data is not None
            and len(edge_data) > 0
            and "label" in edge_data[0]
        ):
            edge_data[0]["label"] = (
                re.sub("\(.*?\)", "", edge_data[0]["label"]).strip('"').strip()
            )

    return new_graph


def convert_dot_str_to_networkx_graph(dot_str: str) -> Graph:
    graphs = pydot.graph_from_dot_data(dot_str)  # convert to Pydot Objects
    networkx_grapg = nx_pydot.from_pydot(graphs[0])
    return edit_edge_labels(networkx_grapg)


def get_dict_from_graph(g: Graph) -> Any:
    return json_graph.node_link_data(g)


def get_root_node_in_digraph(g: Graph, is_forward: bool) -> Optional[Any]:
    if len(g.nodes) == 0:
        return None
    degrees = g.in_degree() if is_forward else g.out_degree()
    root = [n for n, d in degrees if d == 0]
    return root


def get_end_goal_node_in_digraph(g: Graph) -> Optional[Any]:
    if len(g.nodes) == 0:
        return None
    end_goal = [n for n, d in g.out_degree() if d == 0]
    return end_goal[0]


def get_edge_label(g: Graph, edge: Any) -> Optional[str]:
    if len(g.nodes) == 0:
        return None
    edge_data = g.get_edge_data(edge[0], edge[1])
    edge_label: str = edge_data[0]["label"].replace('"', "").strip().lower()
    return edge_label


def get_first_node_with_multiple_out_edges(
    g: Graph,
    is_forward: bool = True,
) -> List[Tuple[Any, List[Any], List[Any]]]:
    """
    returns a list of tuples of 1) node with multiple out edges, 2) first achiever in the node, 3) out edges from the node, and 4) edges traversed up to the node
    """
    if len(g.nodes) == 0:
        return None
    root: Optional[Any] = None
    # find a node to start
    roots = get_root_node_in_digraph(g, is_forward)
    queue: List[Tuple[Any, List[Any]]] = list()
    queue.extend(list(map(lambda root: (root, []), roots)))
    # edges_traversed: List[Any] = list()
    nodes_with_multiple_edges: List[Tuple[Any, List[Any], List[Any]]] = list()
    nodes_visited: Set[Any] = set()
    while len(queue) > 0:
        new_queue: List[Any] = list()
        for node, edges_traversed in queue:
            edges = (
                list(g.out_edges(node))
                if is_forward
                else list(g.in_edges(node))
            )

            if len(edges) > 1 and node not in nodes_visited:
                nodes_with_multiple_edges.append(
                    (
                        deepcopy(node),
                        deepcopy(edges),
                        deepcopy(edges_traversed),
                    )
                )
                nodes_visited.add(node)
                continue
            for edge in edges:
                edge_label = get_edge_label(g, edge)
                edges_traversed_so_far = edges_traversed + [edge_label]
                new_queue.append(
                    (edge[1], deepcopy(edges_traversed_so_far))
                    if is_forward
                    else (edge[0], deepcopy(edges_traversed_so_far))
                )

            nodes_visited.add(node)
        queue = new_queue
    return nodes_with_multiple_edges


def get_landmarks_in_edges(
    g: Graph,
    edges: List[Any],
    landmarks: List[Landmark],
) -> List[Landmark]:
    # TODO TEST THIS
    edge_label_landmark_dict: Dict[str, List[Landmark]] = dict()
    for landmark in landmarks:
        if len(landmark.first_achievers) > 0:
            for first_achiever in landmark.first_achievers:
                if first_achiever not in edge_label_landmark_dict:
                    edge_label_landmark_dict[first_achiever] = list()
                edge_label_landmark_dict[first_achiever].append(landmark)

    selectable_landmarks: List[Landmark] = list()
    first_achiever_edge_dict: Dict[str, Tuple(str, str)] = dict()
    for edge in edges:
        edge_label = get_edge_label(g, edge)
        if edge_label in edge_label_landmark_dict:
            first_achiever_edge_dict[edge_label] = deepcopy(edge)
            for landmark in edge_label_landmark_dict[edge_label]:
                selectable_landmarks.append(landmark.copy(deep=True))
    return selectable_landmarks, first_achiever_edge_dict


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


def get_node_distance_from_terminal_node(
    g: Graph, is_forward: bool
) -> Dict[str, int]:
    """
    returns a dictionary of node names (keys) and lists of plan hashes
    """
    node_distance_from_terminal_node_dict: Dict[str] = dict()

    if len(g.nodes) == 0:
        return node_distance_from_terminal_node_dict

    start_nodes = get_root_node_in_digraph(g, is_forward)
    queue: List[Any] = list()
    queue.extend(start_nodes)
    depth = 0

    while len(queue) > 0:
        new_queue: List[Any] = list()
        for node in queue:
            edges = (
                list(g.out_edges(node))
                if is_forward
                else list(g.in_edges(node))
            )
            if node not in node_distance_from_terminal_node_dict:
                node_distance_from_terminal_node_dict[node] = depth
            for edge in edges:
                target_node = edge[1] if is_forward else edge[0]
                new_queue.append(target_node)
        depth += 1
        queue = new_queue

    return node_distance_from_terminal_node_dict


def get_node_edge_name_plan_hash_list(
    g: Graph, plans: List[Plan], is_forward: bool
) -> Tuple[
    Dict[str, List[str]],
    Dict[Tuple[Any, Any], List[str]],
    Dict[str, List[str]],
]:
    """
    returns a dictionary of node names (keys) and lists of plan hashes
    """
    if len(g.nodes) == 0:
        return {}, {}, {}

    start_nodes = get_root_node_in_digraph(g, is_forward)
    node_list_plan_hash_dict: Dict[str, List[str]] = dict()
    edge_list_plan_hash_dict: Dict[Tuple[Any, Any], List[str]] = dict()
    edge_label_nodes_set_dict: Dict[
        str, Set[str]
    ] = dict()  # a Dictionary of edge labels and sets of nodes
    queue: List[Any] = list()
    queue.extend(start_nodes)
    depth = 0
    while len(queue) > 0:
        new_queue: List[Any] = list()
        for node in queue:
            edges = (
                list(g.out_edges(node))
                if is_forward
                else list(g.in_edges(node))
            )
            plan_hashes_for_node: set[str] = set()
            for edge in edges:
                edge_label = get_edge_label(g, edge)
                if edge_label not in edge_label_nodes_set_dict:
                    edge_label_nodes_set_dict[edge_label] = set()
                edge_label_nodes_set_dict[edge_label].add(node)

                for plan in plans:
                    if depth < len(plan.actions):
                        if edge_label in plan.actions[depth]:
                            plan_hashes_for_node.add(plan.plan_hash[:])
                            if edge not in edge_list_plan_hash_dict:
                                edge_list_plan_hash_dict[edge] = list()
                            edge_list_plan_hash_dict[edge].append(
                                plan.plan_hash[:]
                            )
                target_node = edge[1] if is_forward else edge[0]
                new_queue.append(target_node)
            node_list_plan_hash_dict[node] = list(plan_hashes_for_node)
        depth += 1
        queue = new_queue

    return (
        node_list_plan_hash_dict,
        edge_list_plan_hash_dict,
        {
            edge_label: list(nodes)
            for edge_label, nodes in edge_label_nodes_set_dict.items()
        },
    )


def get_graph_with_number_of_plans_label(
    g: Graph,
    node_list_plan_hash_dict: Dict[str, List[str]],
) -> Graph:
    """
    returns a deep copy of a graph with "num_plans" attribute
    """
    graph_with_new_attributes = g.copy()
    if len(g.nodes) == 0:
        return graph_with_new_attributes
    node_attributes: Dict[str, Dict[str, Any]] = {
        node: {
            "num_plans": len(plan_hashes),
            "plan_hashes": deepcopy(plan_hashes),
        }
        for node, plan_hashes in node_list_plan_hash_dict.items()
    }

    set_node_attributes(graph_with_new_attributes, node_attributes)

    return graph_with_new_attributes
