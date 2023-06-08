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
from helpers.plan_disambiguator_helper.selection_flow_helper import (
    get_selection_flow_output,
)


class TestSelectionFlowHelper(unittest.TestCase):
    gripper_domain: str
    gripper_problem: str
    gripper_landmarks: List[Landmark]
    planner_response_model: PlannerResponseModel

    @classmethod
    def setUpClass(cls) -> None:
        TestSelectionFlowHelper.gripper_domain = read_str_from_file(
            "./tests/data/pddl/gripper/domain.pddl"
        )
        TestSelectionFlowHelper.gripper_problem = read_str_from_file(
            "./tests/data/pddl/gripper/problem.pddl"
        )
        TestSelectionFlowHelper.gripper_landmarks = (
            get_landmarks_by_landmark_category(
                TestSelectionFlowHelper.gripper_domain,
                TestSelectionFlowHelper.gripper_problem,
                LandmarkCategory.RWH,
            )
        )
        TestSelectionFlowHelper.planner_response_model = (
            PlannerResponseModel.parse_obj(
                asdict(
                    get_plan_topq(
                        TestSelectionFlowHelper.gripper_domain,
                        TestSelectionFlowHelper.gripper_problem,
                        6,
                        1.0,
                    )
                )
            )
        )
        TestSelectionFlowHelper.planner_response_model.set_plan_hashes()

    def test_get_selection_flow_output_no_selected_landmarks(self) -> None:
        selected_landmark_0 = SelelctionInfo(
            facts=["Atom carry(ball2, left)", "Atom carry(ball2, right)"],
            disjunctive=True,
            selected_first_achiever="pick ball2 rooma right",
        )
        selection_flow_output = get_selection_flow_output(
            [selected_landmark_0],
            TestSelectionFlowHelper.gripper_landmarks,
            TestSelectionFlowHelper.gripper_domain,
            TestSelectionFlowHelper.gripper_problem,
            TestSelectionFlowHelper.planner_response_model.plans,
        )
        self.assertEqual(len(selection_flow_output.plans), 3)
        self.assertEqual(len(selection_flow_output.choice_infos), 3)
        self.assertEqual(len(selection_flow_output.networkx_graph), 5)

    def test_get_selection_flow_output_no_landmarks_no_selection_info(
        self,
    ) -> None:
        selection_flow_output = get_selection_flow_output(
            [],
            [],
            TestSelectionFlowHelper.gripper_domain,
            TestSelectionFlowHelper.gripper_problem,
            TestSelectionFlowHelper.planner_response_model.plans,
        )
        self.assertEqual(len(selection_flow_output.plans), 6)
        self.assertEqual(len(selection_flow_output.choice_infos), 1)
        self.assertIsNone(selection_flow_output.choice_infos[0].landmark)
        self.assertIsNone(selection_flow_output.choice_infos[0].max_num_plans)
        self.assertIsNone(
            selection_flow_output.choice_infos[0].action_name_plan_idx_map
        )
        self.assertEqual(
            selection_flow_output.choice_infos[0].node_with_multiple_out_edges,
            "node0",
        )
        self.assertEqual(
            len(
                selection_flow_output.choice_infos[0].action_name_plan_hash_map
            ),
            4,
        )
        self.assertEqual(len(selection_flow_output.networkx_graph), 5)
