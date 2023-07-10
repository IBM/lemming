from dataclasses import asdict
from typing import List

import unittest
import os

from helpers.common_helper.file_helper import read_str_from_file
from helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topq,
)
from helpers.planner_helper.planner_helper_data_types import (
    LandmarkCategory,
    SelectionInfo,
    PlannerResponseModel,
    Landmark,
    PlanningTask,
    ChoiceInfo,
)
from helpers.plan_disambiguator_helper.plan_disambiguator_helper import (
    get_plans_with_selection_infos,
    get_split_by_actions,
    get_plan_disambiguator_output_filtered_by_selection_infos,
    get_plans_filetered_by_selected_plan_hashes,
    get_plan_idx_edge_dict,
    get_edge_label_plan_hashes_dict,
    append_landmarks_not_available_for_choice,
    get_min_dist_between_nodes_from_terminal_node,
)

my_dir = os.path.dirname(__file__)
rel_pddl_path = "../../data/pddl/{}.pddl"


class TestPlanDisambiguatorHelper(unittest.TestCase):
    gripper_domain: str
    gripper_problem: str
    gripper_landmarks: List[Landmark]
    planner_response_model: PlannerResponseModel

    @classmethod
    def setUpClass(cls) -> None:
        TestPlanDisambiguatorHelper.gripper_domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("gripper/domain"))
        )
        TestPlanDisambiguatorHelper.gripper_problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("gripper/problem"))
        )
        TestPlanDisambiguatorHelper.gripper_landmarks = (
            get_landmarks_by_landmark_category(
                PlanningTask(
                    domain=TestPlanDisambiguatorHelper.gripper_domain,
                    problem=TestPlanDisambiguatorHelper.gripper_problem,
                ),
                LandmarkCategory.RWH.value,
            )
        )
        TestPlanDisambiguatorHelper.planner_response_model = (
            PlannerResponseModel.parse_obj(
                asdict(
                    get_plan_topq(
                        PlanningTask(
                            domain=TestPlanDisambiguatorHelper.gripper_domain,
                            problem=TestPlanDisambiguatorHelper.gripper_problem,
                            num_plans=6,
                            quality_bound=1.0,
                        )
                    )
                )
            )
        )
        TestPlanDisambiguatorHelper.planner_response_model.set_plan_hashes()

    def test_get_plans_with_selection_infos(self) -> None:
        selection_info_0 = SelectionInfo(
            selected_plan_hashes=[
                "6a81b2a65657b4444a989205b590c346",
                "9d49f737b4735da2a3b0d85e3be0bf67",
            ],
        )
        selection_info_1 = SelectionInfo(
            selected_plan_hashes=["9d49f737b4735da2a3b0d85e3be0bf67"],
        )
        selected_plans = get_plans_with_selection_infos(
            [selection_info_0, selection_info_1],
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        # before selection
        self.assertEqual(
            len(TestPlanDisambiguatorHelper.planner_response_model.plans), 6
        )
        # after selection
        self.assertEqual(len(selected_plans), 1)

    def test_get_split_by_actions(self) -> None:
        expected_dict_0 = {
            "drop ball1 roomb left": [0, 1, 4],
            "drop ball1 roomb right": [2, 3, 5],
        }
        expected_dict_1 = {
            "pick ball4 rooma left": [0, 2, 5],
            "pick ball4 rooma right": [1, 3, 4],
        }
        landmark_infos = get_split_by_actions(
            TestPlanDisambiguatorHelper.gripper_landmarks,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
            {},
        )
        self.assertEqual(len(landmark_infos), 8)
        self.assertEqual(landmark_infos[0].max_num_plans, 3)
        self.assertEqual(
            landmark_infos[0].action_name_plan_idx_map, expected_dict_0
        )
        self.assertEqual(landmark_infos[-1].max_num_plans, 3)
        self.assertEqual(
            landmark_infos[-1].action_name_plan_idx_map, expected_dict_1
        )

    def test_get_plan_disambiguator_output_filtered_by_selection_infos(
        self,
    ) -> None:
        selected_landmark_0 = SelectionInfo(
            selected_first_achiever="pick ball2 rooma right",
            selected_plan_hashes=["9d49f737b4735da2a3b0d85e3be0bf67"],
        )
        (
            selected_plans,
            landmark_infos,
            g,
            _,
            node_plan_hashes_dict,
            edge_plan_hash_dict,
            edge_label_nodes_dict,
            node_dist_from_initial_state,
            node_dist_from_end_state,
        ) = get_plan_disambiguator_output_filtered_by_selection_infos(
            [selected_landmark_0],
            TestPlanDisambiguatorHelper.gripper_landmarks,
            TestPlanDisambiguatorHelper.gripper_domain,
            TestPlanDisambiguatorHelper.gripper_problem,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(selected_plans), 1)
        self.assertEqual(len(landmark_infos), 0)
        self.assertEqual(g.name, "G")

    def test_get_plans_filetered_by_selected_plan_hashes_no_plan_hash(
        self,
    ) -> None:
        selected_landmark = SelectionInfo(selected_plan_hashes=[])
        plans = get_plans_filetered_by_selected_plan_hashes(
            selected_landmark,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(plans), 6)

    def test_get_plans_filetered_by_selected_plan_hashes_none_plan_hash(
        self,
    ) -> None:
        selected_landmark = SelectionInfo(selected_plan_hashes=None)
        plans = get_plans_filetered_by_selected_plan_hashes(
            selected_landmark,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(plans), 6)

    def test_get_plans_filetered_by_selected_plan_hashes_valid_plan_hash(
        self,
    ) -> None:
        hashes = [
            "6a81b2a65657b4444a989205b590c346",
            "a30b377144530876cd5506f0df8a1f16",
            "aaaaa",
        ]
        selected_landmark = SelectionInfo(selected_plan_hashes=hashes)
        plans = get_plans_filetered_by_selected_plan_hashes(
            selected_landmark,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(plans), 2)

    def test_get_plan_idx_edge_dict_forward(self) -> None:
        plan_idx_action_dict = get_plan_idx_edge_dict(
            [("a", "b"), ("b", "c"), ("c", "d")],
            TestPlanDisambiguatorHelper.planner_response_model.plans,
            True,
        )
        self.assertEqual(
            plan_idx_action_dict,
            {
                0: "drop ball2 roomb right",
                1: "drop ball2 roomb right",
                2: "drop ball1 roomb right",
                3: "drop ball2 roomb left",
                4: "drop ball3 roomb right",
                5: "drop ball1 roomb right",
            },
        )

    def test_get_plan_idx_edge_dict_backward(self) -> None:
        plan_idx_action_dict = get_plan_idx_edge_dict(
            [("a", "b"), ("b", "c"), ("c", "d")],
            TestPlanDisambiguatorHelper.planner_response_model.plans,
            False,
        )
        self.assertEqual(
            plan_idx_action_dict,
            {
                0: "pick ball4 rooma left",
                1: "pick ball3 rooma left",
                2: "pick ball4 rooma left",
                3: "pick ball4 rooma right",
                4: "pick ball2 rooma left",
                5: "pick ball4 rooma left",
            },
        )

    def test_get_edge_label_plan_hashes_dict(self) -> None:
        edge_label_plan_hash_dict = get_edge_label_plan_hashes_dict(
            [("a", "b"), ("b", "c"), ("c", "d")],
            TestPlanDisambiguatorHelper.planner_response_model.plans,
            True,
        )
        self.assertEqual(
            edge_label_plan_hash_dict,
            {
                "drop ball2 roomb right": [
                    "6a81b2a65657b4444a989205b590c346",
                    "9d49f737b4735da2a3b0d85e3be0bf67",
                ],
                "drop ball1 roomb right": [
                    "08ef565ec364978b0295105f8ae52bce",
                    "f7f6db06a380e59c52ab115b2d771988",
                ],
                "drop ball2 roomb left": ["a30b377144530876cd5506f0df8a1f16"],
                "drop ball3 roomb right": ["80af1fcf0d421d8bfc7bf4751a6ee24c"],
            },
        )

    def test_append_landmarks_not_available_for_choice(self) -> None:
        landmark = Landmark(facts=["b"])
        landmarks = [
            Landmark(facts=["a"], first_achievers=["sadadas", "asdasdsad"]),
            landmark,
        ]
        choice_infos = [ChoiceInfo(landmark=landmark)]
        new_choice_infos = append_landmarks_not_available_for_choice(
            landmarks, choice_infos
        )
        self.assertEqual(len(new_choice_infos), 2)
        self.assertTrue(new_choice_infos[0].is_available_for_choice)
        self.assertFalse(new_choice_infos[1].is_available_for_choice)

    def test_get_min_dist_between_nodes_from_terminal_node(self) -> None:
        label_a = "label_a"
        label_b = "label_b"
        edge_labels = [label_a, label_b]
        node_0 = "node_0"
        node_1 = "node_1"
        node_2 = "node_2"
        edge_label_nodes_dict = {label_a: [node_0, node_1], label_b: [node_2]}
        min_val = 11
        node_dist_from_terminal_state = {
            node_0: 111,
            node_1: min_val,
            node_2: 1111,
        }
        res = get_min_dist_between_nodes_from_terminal_node(
            edge_labels, edge_label_nodes_dict, node_dist_from_terminal_state
        )
        self.assertEqual(res, min_val)
