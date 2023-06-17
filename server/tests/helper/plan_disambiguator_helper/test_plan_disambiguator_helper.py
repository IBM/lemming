import os
import unittest
from dataclasses import asdict
from typing import List

from helpers.common_helper.file_helper import read_str_from_file
from helpers.plan_disambiguator_helper.plan_disambiguator_helper import (
    append_landmarks_not_available_for_choice,
    get_edge_label_plan_hashes_dict,
    get_filtered_out_selection_infos_by_selection_infos,
    get_plan_disambiguator_output_filtered_by_selection_infos,
    get_plan_idx_edge_dict,
    get_plans_filetered_by_selected_plan_hashes,
    get_plans_with_selection_info,
    get_plans_with_selection_infos,
    get_split_by_actions,
)
from helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topq,
)
from helpers.planner_helper.planner_helper_data_types import (
    ChoiceInfo,
    Landmark,
    LandmarkCategory,
    PlannerResponseModel,
    PlanningTask,
    SelelctionInfo,
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

    def test_get_plans_with_selection_info(self) -> None:
        selected_landmark = SelelctionInfo(
            facts=["Atom at(ball1, roomb)"],
            disjunctive=False,
            selected_first_achiever="drop ball1 roomb left",
        )
        selected_plans = get_plans_with_selection_info(
            selected_landmark,
            TestPlanDisambiguatorHelper.gripper_landmarks,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        # before selection
        self.assertEqual(
            len(TestPlanDisambiguatorHelper.planner_response_model.plans), 6
        )
        # after selection
        self.assertEqual(len(selected_plans), 3)

    def test_get_filtered_out_selection_infos_by_selection_infos(self) -> None:
        selected_landmark_0 = SelelctionInfo(
            facts=["Atom at(ball1, roomb)"],
            disjunctive=False,
            selected_first_achiever="drop ball1 roomb left",
        )
        filtered_landmarks = (
            get_filtered_out_selection_infos_by_selection_infos(
                TestPlanDisambiguatorHelper.gripper_landmarks,
                [selected_landmark_0],
            )
        )
        self.assertEqual(len(filtered_landmarks), 11)

    def test_get_plans_with_selection_infos(self) -> None:
        selected_landmark_0 = SelelctionInfo(
            facts=["Atom at(ball1, roomb)"],
            disjunctive=False,
            selected_first_achiever="drop ball1 roomb left",
        )
        selected_landmark_1 = SelelctionInfo(
            facts=["Atom at(ball3, roomb)"],
            disjunctive=False,
            selected_first_achiever="drop ball3 roomb right",
        )
        selected_plans = get_plans_with_selection_infos(
            [selected_landmark_0, selected_landmark_1],
            TestPlanDisambiguatorHelper.gripper_landmarks,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        # before selection
        self.assertEqual(
            len(TestPlanDisambiguatorHelper.planner_response_model.plans), 6
        )
        # after selection
        self.assertEqual(len(selected_plans), 2)

    def test_get_split_by_actions(self) -> None:
        expected_dict_0 = {
            "drop ball1 roomb left": [0, 1, 4],
            "drop ball1 roomb right": [2, 3, 5],
        }
        expected_dict_1 = {"move roomb rooma": [0, 1, 2, 3, 4, 5]}
        landmark_infos = get_split_by_actions(
            TestPlanDisambiguatorHelper.gripper_landmarks,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(landmark_infos[0].max_num_plans, 3)
        self.assertEqual(
            landmark_infos[0].action_name_plan_idx_map, expected_dict_0
        )
        self.assertEqual(landmark_infos[-1].max_num_plans, 6)
        self.assertEqual(
            landmark_infos[-1].action_name_plan_idx_map, expected_dict_1
        )

    def test_get_plan_disambiguator_output_filtered_by_selection_infos(
        self,
    ) -> None:
        selected_landmark_0 = SelelctionInfo(
            facts=["Atom carry(ball2, left)", "Atom carry(ball2, right)"],
            disjunctive=True,
            selected_first_achiever="pick ball2 rooma right",
        )
        (
            selected_plans,
            landmark_infos,
            g,
            _,
            node_plan_hashes_dict,
        ) = get_plan_disambiguator_output_filtered_by_selection_infos(
            [selected_landmark_0],
            TestPlanDisambiguatorHelper.gripper_landmarks,
            TestPlanDisambiguatorHelper.gripper_domain,
            TestPlanDisambiguatorHelper.gripper_problem,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(selected_plans), 3)
        self.assertEqual(len(landmark_infos), 7)
        self.assertEqual(g.name, "G")

    def test_get_plans_filetered_by_selected_plan_hashes_no_plan_hash(
        self,
    ) -> None:
        selected_landmark = SelelctionInfo(selected_plan_hashes=[])
        plans = get_plans_filetered_by_selected_plan_hashes(
            selected_landmark,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(plans), 6)

    def test_get_plans_filetered_by_selected_plan_hashes_none_plan_hash(
        self,
    ) -> None:
        selected_landmark = SelelctionInfo(selected_plan_hashes=None)
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
        selected_landmark = SelelctionInfo(selected_plan_hashes=hashes)
        plans = get_plans_filetered_by_selected_plan_hashes(
            selected_landmark,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(plans), 2)

    def test_get_plans_with_selection_info_1(self) -> None:
        hashes = [
            "6a81b2a65657b4444a989205b590c346",
            "a30b377144530876cd5506f0df8a1f16",
        ]
        selected_landmark = SelelctionInfo(selected_plan_hashes=hashes)
        plans = get_plans_with_selection_info(
            selected_landmark,
            TestPlanDisambiguatorHelper.gripper_landmarks,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(plans), 2)

    def test_get_plans_with_selection_info_2(self) -> None:
        selected_landmark = SelelctionInfo(
            facts=["Atom carry(ball2, left)", "Atom carry(ball2, right)"],
            disjunctive=True,
            selected_first_achiever="pick ball2 rooma right",
        )
        plans = get_plans_with_selection_info(
            selected_landmark,
            TestPlanDisambiguatorHelper.gripper_landmarks,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(plans), 3)

    def test_get_plans_with_selection_infos_1(self) -> None:
        selected_landmark_0 = SelelctionInfo(
            facts=["Atom carry(ball2, left)", "Atom carry(ball2, right)"],
            disjunctive=True,
            selected_first_achiever="pick ball2 rooma right",
        )
        hashes = [
            "6a81b2a65657b4444a989205b590c346",
            "a30b377144530876cd5506f0df8a1f16",
        ]
        selected_landmark_1 = SelelctionInfo(selected_plan_hashes=hashes)
        plans = get_plans_with_selection_infos(
            [selected_landmark_0, selected_landmark_1],
            TestPlanDisambiguatorHelper.gripper_landmarks,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0].plan_hash, "6a81b2a65657b4444a989205b590c346")

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
        landmarks = [Landmark(facts=["a"]), landmark]
        choice_infos = [ChoiceInfo(landmark=landmark)]
        new_choice_infos = append_landmarks_not_available_for_choice(
            landmarks, choice_infos
        )
        self.assertEqual(len(new_choice_infos), 2)
        self.assertTrue(new_choice_infos[0].is_available_for_choice)
        self.assertFalse(new_choice_infos[1].is_available_for_choice)
