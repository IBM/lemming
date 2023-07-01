from dataclasses import asdict
from typing import List
import unittest
import os

from pydot import Dot, Edge, Node
import networkx as nx
from helpers.graph_helper.graph_helper import (
    convert_dot_str_to_networkx_graph,
    get_dict_from_graph,
    get_root_node_in_digraph,
    get_end_goal_node_in_digraph,
    get_first_node_with_multiple_out_edges,
    get_all_nodes_coming_from_node,
    get_nodes_to_exclude,
    get_graph_with_number_of_plans_label,
    get_edge_label,
)
from helpers.planner_helper.planner_helper_data_types import (
    Landmark,
    LandmarkCategory,
    PlannerResponseModel,
    PlanningTask,
)
from helpers.common_helper.file_helper import read_str_from_file
from helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topq,
)
from helpers.plan_disambiguator_helper.plan_disambiguator_helper import (
    get_plan_disambiguator_output_filtered_by_selection_infos,
)


my_dir = os.path.dirname(__file__)
rel_dot_path = "../../data/graph/{}.dot"
rel_pddl_path = "../../data/pddl/{}.pddl"


class TestGraphHelper(unittest.TestCase):
    gripper_domain: str
    gripper_problem: str
    gripper_landmarks: List[Landmark]
    planner_response_model: PlannerResponseModel
    test_graph: nx.Graph

    @classmethod
    def setUpClass(cls) -> None:
        TestGraphHelper.gripper_domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("gripper/domain"))
        )
        TestGraphHelper.gripper_problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("gripper/problem"))
        )
        TestGraphHelper.gripper_landmarks = get_landmarks_by_landmark_category(
            PlanningTask(
                domain=TestGraphHelper.gripper_domain,
                problem=TestGraphHelper.gripper_problem,
            ),
            LandmarkCategory.RWH.value,
        )
        TestGraphHelper.planner_response_model = PlannerResponseModel.parse_obj(
            asdict(
                get_plan_topq(
                    PlanningTask(
                        domain=TestGraphHelper.gripper_domain,
                        problem=TestGraphHelper.gripper_problem,
                        num_plans=6,
                        quality_bound=1.0,
                    )
                )
            )
        )
        TestGraphHelper.planner_response_model.set_plan_hashes()
        (
            _,
            _,
            TestGraphHelper.test_graph,
            _,
            _,
            _,
        ) = get_plan_disambiguator_output_filtered_by_selection_infos(
            [],
            TestGraphHelper.gripper_landmarks,
            TestGraphHelper.gripper_domain,
            TestGraphHelper.gripper_problem,
            TestGraphHelper.planner_response_model.plans,
        )

    def test_convert_dot_str_to_networkx_graph(self) -> None:
        dot_string = """graph {
                    a -- b;
                    b -- c;
                } """

        nx_graph = convert_dot_str_to_networkx_graph(dot_string)
        self.assertIsNotNone(nx_graph)

    def test_pydot_networkx_conversion(self) -> None:
        graph = Dot(graph_type="digraph")
        # graph = Dot(graph_type="graph")
        graph.add_edge(Edge("1", "2"))
        graph.add_edge(Edge("2", "4"))
        graph.add_edge(Edge("4", "5"))
        graph.add_edge(Edge("1", "3"))
        # orphan node
        graph.add_node(
            Node(name="a", label="AA", style="filled", fillcolor="green")
        )
        # graph.write_png("sample.png")
        _ = nx.nx_pydot.from_pydot(graph)  # return MultiGraph
        assert True

    def test_networkx(self) -> None:
        K5 = nx.complete_graph(5)
        A = nx.nx_pydot.to_pydot(K5)  # conversion to pydot
        _ = nx.nx_pydot.from_pydot(A)  # return MultiGraph

    def test_read_dot_file(self) -> None:
        abs_path_to_dot_file = os.path.join(
            my_dir, rel_dot_path.format("example")
        )
        _ = nx.nx_pydot.read_dot(abs_path_to_dot_file)

    def test_nx_basics(self) -> None:
        G = nx.Graph()
        G.add_node(1)
        G.add_nodes_from([2, 3])
        G.add_nodes_from([(4, {"color": "red"})])

    def test_graph_conversion(self) -> None:
        dot_str = ""
        abs_path_to_dot_file = os.path.join(
            my_dir, rel_dot_path.format("sample")
        )
        with open(abs_path_to_dot_file, "r") as f:
            dot_str = f.read()
        g = convert_dot_str_to_networkx_graph(dot_str)
        graph_dict = get_dict_from_graph(g)
        self.assertEqual(len(graph_dict), 5)

    def test_get_root_node_in_digraph(self) -> None:
        dot_str = ""
        abs_path_to_dot_file = os.path.join(
            my_dir, rel_dot_path.format("sample")
        )
        with open(abs_path_to_dot_file, "r") as f:
            dot_str = f.read()
        g = convert_dot_str_to_networkx_graph(dot_str)
        root = get_root_node_in_digraph(g, True)
        self.assertEqual(root[0], "node0")

    def test_get_end_goal_node_in_digraph(self) -> None:
        dot_str = ""
        abs_path_to_dot_file = os.path.join(
            my_dir, rel_dot_path.format("sample")
        )
        with open(abs_path_to_dot_file, "r") as f:
            dot_str = f.read()
        g = convert_dot_str_to_networkx_graph(dot_str)
        root = get_end_goal_node_in_digraph(g)
        self.assertEqual(root, "node11")

    def test_traversal(self) -> None:
        dot_str = ""
        abs_path_to_dot_file = os.path.join(
            my_dir, rel_dot_path.format("sample")
        )
        with open(abs_path_to_dot_file, "r") as f:
            dot_str = f.read()
        g = convert_dot_str_to_networkx_graph(dot_str)
        root = get_root_node_in_digraph(g, True)
        res = list(g.out_edges(root))
        self.assertEqual(res, [("node0", "node1")])
        res = list(g.out_edges(res[0][1]))
        self.assertEqual(res, [("node1", "node16"), ("node1", "node2")])

    def test_get_first_node_with_multiple_out_edges_node2(self) -> None:
        dot_str = ""
        abs_path_to_dot_file = os.path.join(
            my_dir, rel_dot_path.format("sample")
        )
        with open(abs_path_to_dot_file, "r") as f:
            dot_str = f.read()
        g = convert_dot_str_to_networkx_graph(dot_str)
        first_achiever_plan_idx_dict = {"pick ball2 rooma right": [0, 1, 5]}
        # (
        #     first_node_with_first_achiever,
        #     first_achiever,
        #     out_edges_first_node_with_first_achiever,
        #     edges_traversed,
        # )

        nodes = get_first_node_with_multiple_out_edges(g, True)
        self.assertEqual(nodes[0][0], "node1")
        self.assertEqual(
            nodes[0][1],
            [("node1", "node16"), ("node1", "node2")],
        )
        self.assertEqual(nodes[0][2], ["pick ball1 rooma left"])

    def test_get_first_node_with_multiple_out_edges_no_first_achiever_found(
        self,
    ) -> None:
        dot_str = ""
        abs_path_to_dot_file = os.path.join(
            my_dir, rel_dot_path.format("sample")
        )
        with open(abs_path_to_dot_file, "r") as f:
            dot_str = f.read()
        g = convert_dot_str_to_networkx_graph(dot_str)
        first_achiever_plan_idx_dict = {"nothing": [0, 1, 5]}
        res = get_first_node_with_multiple_out_edges(g, True)
        self.assertEqual(
            res,
            [
                (
                    "node1",
                    [("node1", "node16"), ("node1", "node2")],
                    ["pick ball1 rooma left"],
                )
            ],
        )

    def test_get_first_node_with_multiple_out_edges_no_first_achiever_found_backward(
        self,
    ) -> None:
        dot_str = ""
        abs_path_to_dot_file = os.path.join(
            my_dir, rel_dot_path.format("sample")
        )
        with open(abs_path_to_dot_file, "r") as f:
            dot_str = f.read()
        g = convert_dot_str_to_networkx_graph(dot_str)
        first_achiever_plan_idx_dict = {"nothing": [0, 1, 5]}
        res = get_first_node_with_multiple_out_edges(g, False)
        self.assertEqual(
            res,
            [
                (
                    "node11",
                    [("node15", "node11"), ("node10", "node11")],
                    [],
                )
            ],
        )

    def test_get_all_nodes_coming_from_node(self) -> None:
        dot_str = ""
        abs_path_to_dot_file = os.path.join(
            my_dir, rel_dot_path.format("sample")
        )
        with open(abs_path_to_dot_file, "r") as f:
            dot_str = f.read()
        g = convert_dot_str_to_networkx_graph(dot_str)
        source_node = "node1"
        nodes = get_all_nodes_coming_from_node(g, source_node, {"node19"}, True)
        self.assertEqual(len(nodes), 17)

    def test_get_nodes_to_exclude(self) -> None:
        dot_str = ""
        abs_path_to_dot_file = os.path.join(
            my_dir, rel_dot_path.format("sample")
        )
        with open(abs_path_to_dot_file, "r") as f:
            dot_str = f.read()
        g = convert_dot_str_to_networkx_graph(dot_str)
        nodes_to_start = "node2"
        nodes_to_exclude = get_nodes_to_exclude(g, {nodes_to_start}, True)
        self.assertEqual(len(nodes_to_exclude), 13)

    def test_get_graph_with_number_of_plans_label(self) -> None:
        node = "node0"
        value = "abcdedfshads"
        g = get_graph_with_number_of_plans_label(
            TestGraphHelper.test_graph, {node: [value]}
        )
        num_plans = g.nodes[node]["num_plans"]
        self.assertEqual(num_plans, 1)

    def test_get_edge_label(self) -> None:
        edge_label = get_edge_label(
            TestGraphHelper.test_graph, ("node38", "node39")
        )
        self.assertEqual(edge_label, "drop ball4 roomb left")
