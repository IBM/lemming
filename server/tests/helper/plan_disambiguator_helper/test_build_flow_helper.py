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
    PlanningTask,
    PlannerResponseModel,
    LandmarkCategory,
    Landmark,
)
from helpers.plan_disambiguator_helper.build_flow_helper import (
    get_build_forward_flow_output,
)

my_dir = os.path.dirname(__file__)
rel_pddl_path = "../../data/pddl/{}.pddl"


class TestBuildFlowHelper(unittest.TestCase):
    gripper_domain: str
    gripper_problem: str
    gripper_landmarks: List[Landmark]
    planner_response_model: PlannerResponseModel

    @classmethod
    def setUpClass(cls) -> None:
        TestBuildFlowHelper.gripper_domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("gripper/domain"))
        )
        TestBuildFlowHelper.gripper_problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("gripper/problem"))
        )
        TestBuildFlowHelper.gripper_landmarks = (
            get_landmarks_by_landmark_category(
                PlanningTask(
                    domain=TestBuildFlowHelper.gripper_domain,
                    problem=TestBuildFlowHelper.gripper_problem,
                ),
                LandmarkCategory.RWH.value,
            )
        )
        TestBuildFlowHelper.planner_response_model = (
            PlannerResponseModel.parse_obj(
                asdict(
                    get_plan_topq(
                        PlanningTask(
                            domain=TestBuildFlowHelper.gripper_domain,
                            problem=TestBuildFlowHelper.gripper_problem,
                            num_plans=6,
                            quality_bound=1.0,
                        )
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
