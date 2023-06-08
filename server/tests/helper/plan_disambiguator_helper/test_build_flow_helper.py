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
    PlannerResponseModel,
    Landmark,
)
from helpers.plan_disambiguator_helper.build_flow_helper import (
    get_build_forward_flow_output,
)


class TestBuildFlowHelper(unittest.TestCase):
    gripper_domain: str
    gripper_problem: str
    gripper_landmarks: List[Landmark]
    planner_response_model: PlannerResponseModel

    @classmethod
    def setUpClass(cls) -> None:
        TestBuildFlowHelper.gripper_domain = read_str_from_file(
            "./tests/data/pddl/gripper/domain.pddl"
        )
        TestBuildFlowHelper.gripper_problem = read_str_from_file(
            "./tests/data/pddl/gripper/problem.pddl"
        )
        TestBuildFlowHelper.gripper_landmarks = (
            get_landmarks_by_landmark_category(
                TestBuildFlowHelper.gripper_domain,
                TestBuildFlowHelper.gripper_problem,
                LandmarkCategory.RWH,
            )
        )
        TestBuildFlowHelper.planner_response_model = (
            PlannerResponseModel.parse_obj(
                asdict(
                    get_plan_topq(
                        TestBuildFlowHelper.gripper_domain,
                        TestBuildFlowHelper.gripper_problem,
                        6,
                        1.0,
                    )
                )
            )
        )
        TestBuildFlowHelper.planner_response_model.set_plan_hashes()

    def test_get_build_forward_flow_output_no_selection_info_no_landmark(
        self,
    ) -> None:
        build_forward_flow_output = get_build_forward_flow_output(
            [],
            [],
            TestBuildFlowHelper.gripper_domain,
            TestBuildFlowHelper.gripper_problem,
            TestBuildFlowHelper.planner_response_model.plans,
        )
        self.assertEqual(len(build_forward_flow_output.plans), 6)
        self.assertEqual(len(build_forward_flow_output.choice_infos), 1)
        self.assertIsNone(build_forward_flow_output.choice_infos[0].landmark)
        self.assertIsNone(
            build_forward_flow_output.choice_infos[0].max_num_plans
        )
        self.assertIsNone(
            build_forward_flow_output.choice_infos[0].action_name_plan_idx_map
        )
        self.assertEqual(
            build_forward_flow_output.choice_infos[
                0
            ].node_with_multiple_out_edges,
            "node0",
        )
        self.assertEqual(
            len(
                build_forward_flow_output.choice_infos[
                    0
                ].action_name_plan_hash_map
            ),
            4,
        )
        self.assertEqual(len(build_forward_flow_output.networkx_graph), 5)

    def test_get_build_forward_flow_output_no_selection_info(self) -> None:
        build_forward_flow_output = get_build_forward_flow_output(
            [],
            TestBuildFlowHelper.gripper_landmarks,
            TestBuildFlowHelper.gripper_domain,
            TestBuildFlowHelper.gripper_problem,
            TestBuildFlowHelper.planner_response_model.plans,
        )
        self.assertEqual(len(build_forward_flow_output.plans), 6)
        self.assertEqual(len(build_forward_flow_output.choice_infos), 1)
        self.assertIsNotNone(build_forward_flow_output.choice_infos[0].landmark)
        self.assertEqual(
            build_forward_flow_output.choice_infos[0].max_num_plans, 3
        )
        self.assertEqual(
            len(
                build_forward_flow_output.choice_infos[
                    0
                ].action_name_plan_idx_map
            ),
            2,
        )
        self.assertIsNone(
            build_forward_flow_output.choice_infos[
                0
            ].node_with_multiple_out_edges
        )
        self.assertEqual(
            len(
                build_forward_flow_output.choice_infos[
                    0
                ].action_name_plan_hash_map
            ),
            2,
        )
        self.assertEqual(len(build_forward_flow_output.networkx_graph), 5)
