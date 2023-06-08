from dataclasses import asdict
from typing import List

import unittest

from helpers.common_helper.file_helper import read_str_from_file
from helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topq,
)
from helpers.planner_helper.planner_helper_data_types import (
    LandmarkCategory,
    SelelctionInfo,
    PlannerResponseModel,
    Landmark,
)
from helpers.plan_disambiguator_helper.plan_disambiguator_helper import (
    get_plans_with_selection_info,
    get_filtered_out_selection_infos_by_selection_infos,
    get_plans_with_selection_infos,
    get_split_by_actions,
    get_plan_disambiguator_output_filtered_by_selection_infos,
)


class TestPlanDisambiguatorHelper(unittest.TestCase):
    gripper_domain: str
    gripper_problem: str
    gripper_landmarks: List[Landmark]
    planner_response_model: PlannerResponseModel

    @classmethod
    def setUpClass(cls) -> None:
        TestPlanDisambiguatorHelper.gripper_domain = read_str_from_file(
            "./tests/data/pddl/gripper/domain.pddl"
        )
        TestPlanDisambiguatorHelper.gripper_problem = read_str_from_file(
            "./tests/data/pddl/gripper/problem.pddl"
        )
        TestPlanDisambiguatorHelper.gripper_landmarks = (
            get_landmarks_by_landmark_category(
                TestPlanDisambiguatorHelper.gripper_domain,
                TestPlanDisambiguatorHelper.gripper_problem,
                LandmarkCategory.RWH,
            )
        )
        TestPlanDisambiguatorHelper.planner_response_model = (
            PlannerResponseModel.parse_obj(
                asdict(
                    get_plan_topq(
                        TestPlanDisambiguatorHelper.gripper_domain,
                        TestPlanDisambiguatorHelper.gripper_problem,
                        6,
                        1.0,
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
        self.assertEqual(len(filtered_landmarks), 4)

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
        ) = get_plan_disambiguator_output_filtered_by_selection_infos(
            [selected_landmark_0],
            TestPlanDisambiguatorHelper.gripper_landmarks,
            TestPlanDisambiguatorHelper.gripper_domain,
            TestPlanDisambiguatorHelper.gripper_problem,
            TestPlanDisambiguatorHelper.planner_response_model.plans,
        )
        self.assertEqual(len(selected_plans), 3)
        self.assertEqual(len(landmark_infos), 3)
        self.assertEqual(g.name, "G")
