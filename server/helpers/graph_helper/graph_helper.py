from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple
import pydot
from networkx import Graph, nx_pydot
from networkx.readwrite import json_graph
from helpers.common_helper.data_type_helper import merge_sets


def convert_dot_str_to_networkx_graph(dot_str: str) -> Graph:
    graphs = pydot.graph_from_dot_data(dot_str)  # convert to Pydot Objects
    return nx_pydot.from_pydot(graphs[0])


def get_dict_from_graph(g: Graph) -> Any:
    return json_graph.node_link_data(g)


def get_root_node_in_digraph(g: Graph) -> Any:
    root = [n for n, d in g.in_degree() if d == 0]
    return root[0]


def get_edge_label(g: Graph, edge: Any) -> str:
    # TODO: TEST THIS
    edge_data = g.get_edge_data(edge[0], edge[1])
    edge_label: str = edge_data[0]["label"].replace('"', "")
    return edge_label


def get_first_node_with_multiple_out_edges_forward(
    g: Graph, first_achiever_plan_idx_dict: Dict[Any, List[Any]]
) -> Optional[Tuple[Any, Optional[Any], List[Any], List[Any]]]:
    """
    returns 1) node with multiple out edges, 2) first achiever in the node, 3) out edges from the node, 4) edges traversed up to the node, and 5) does node contain first achiever out edge
    """
    root = get_root_node_in_digraph(g)
    queue: List[Any] = list()
    queue.append(root)
    edges_traversed: List[Any] = list()
    while len(queue) > 0:
        new_queue: List[Any] = list()
        for node in queue:
            out_edges = list(g.out_edges(node))
            for edge in out_edges:
                edge_label = get_edge_label(g, edge)

                if (
                    len(out_edges) > 1
                    and edge_label in first_achiever_plan_idx_dict
                ):
                    return (
                        deepcopy(node),
                        edge_label,
                        out_edges,
                        edges_traversed,
                    )

                if len(out_edges) == 1:
                    edges_traversed.append(edge_label)

                new_queue.append(edge[1])

            if len(out_edges) > 1:  # out edges are not first achievers
                return deepcopy(node), None, out_edges, edges_traversed

        queue = new_queue
    return None


def get_all_nodes_coming_from_node(
    g: Graph, source_node: Any, nodes_to_exclude: Set[Any] = set()
) -> Set[Any]:
    nodes: Set[Any] = set()
    queue: List[Any] = list()
    queue.append(source_node)
    while len(queue) > 0:
        new_queue: List[Any] = list()
        for node in queue:
            out_edges = list(g.out_edges(node))
            for edge in out_edges:
                if edge[1] not in nodes and edge[1] not in nodes_to_exclude:
                    nodes.add(edge[1])
                    new_queue.append(edge[1])
        queue = new_queue
    return nodes


def get_nodes_to_exclude(g: Graph, nodes_to_start: Set[Any]) -> Set[Any]:
    nodes_to_remove: List[Set[Any]] = list()
    for node_start in nodes_to_start:
        nodes_to_remove.append(get_all_nodes_coming_from_node(g, node_start))

    merger: Set[Any] = merge_sets(nodes_to_remove)
    return merger


def remove_nodes_from_graph(g: Graph, nodes_to_remove: Set[Any]) -> Graph:
    new_graph = g.copy()
    new_graph.remove_nodes_from(list(nodes_to_remove))
    return new_graph


def get_graph_upto_nodes(g: Graph, nodes_to_end: Set[Any]) -> Graph:
    nodes_to_exclude = get_nodes_to_exclude(g, nodes_to_end)
    return remove_nodes_from_graph(g, nodes_to_exclude)
