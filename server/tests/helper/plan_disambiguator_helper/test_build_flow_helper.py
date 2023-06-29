import unittest
import os
from dataclasses import asdict
from typing import List
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
    SelelctionInfo,
)
from helpers.plan_disambiguator_helper.build_flow_helper import (
    get_build_flow_output,
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

        TestBuildFlowHelper.toy_domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("toy/domain"))
        )
        TestBuildFlowHelper.toy_problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("toy/problem"))
        )
        TestBuildFlowHelper.toy_landmarks = get_landmarks_by_landmark_category(
            PlanningTask(
                domain=TestBuildFlowHelper.toy_domain,
                problem=TestBuildFlowHelper.toy_problem,
            ),
            LandmarkCategory.RWH.value,
        )
        TestBuildFlowHelper.toy_planner_response_model = (
            PlannerResponseModel.parse_obj(
                asdict(
                    get_plan_topq(
                        PlanningTask(
                            domain=TestBuildFlowHelper.toy_domain,
                            problem=TestBuildFlowHelper.toy_problem,
                            num_plans=6,
                            quality_bound=1.0,
                        )
                    )
                )
            )
        )
        TestBuildFlowHelper.toy_planner_response_model.set_plan_hashes()

    def test_get_build_forward_flow_output_no_selection_info_no_landmark(
        self,
    ) -> None:
        build_forward_flow_output = get_build_flow_output(
            [],
            [],
            TestBuildFlowHelper.gripper_domain,
            TestBuildFlowHelper.gripper_problem,
            TestBuildFlowHelper.planner_response_model.plans,
            True,
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

    def test_get_build_forward_flow_output_no_selection_info_no_landmark_toy(
        self,
    ) -> None:
        build_forward_flow_output = get_build_flow_output(
            [],
            [],
            TestBuildFlowHelper.toy_domain,
            TestBuildFlowHelper.toy_problem,
            TestBuildFlowHelper.toy_planner_response_model.plans,
            True,
        )
        self.assertEqual(len(build_forward_flow_output.plans), 2)
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
            "node1",
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

    def test_get_build_forward_flow_output_one_selection_info_no_landmark(
        self,
    ) -> None:
        selected_landmark_0 = SelelctionInfo(
            selected_first_achiever="",
            selected_plan_hashes=[
                "08ef565ec364978b0295105f8ae52bce",
                "f7f6db06a380e59c52ab115b2d771988",
            ],
        )
        build_forward_flow_output = get_build_flow_output(
            [selected_landmark_0],
            [],
            TestBuildFlowHelper.gripper_domain,
            TestBuildFlowHelper.gripper_problem,
            TestBuildFlowHelper.planner_response_model.plans,
            True,
        )
        self.assertEqual(len(build_forward_flow_output.plans), 2)
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
            2,
        )
        self.assertEqual(len(build_forward_flow_output.networkx_graph), 5)

    def test_get_build_backword_flow_output_no_selection_info_no_landmark(
        self,
    ) -> None:
        build_forward_flow_output = get_build_flow_output(
            [],
            [],
            TestBuildFlowHelper.gripper_domain,
            TestBuildFlowHelper.gripper_problem,
            TestBuildFlowHelper.planner_response_model.plans,
            False,
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
            "node11",
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

    def test_get_build_backword_flow_output_one_selection_info_no_landmark(
        self,
    ) -> None:
        selected_landmark_0 = SelelctionInfo(
            selected_first_achiever="",
            selected_plan_hashes=[
                "08ef565ec364978b0295105f8ae52bce",
                "f7f6db06a380e59c52ab115b2d771988",
            ],
        )
        build_forward_flow_output = get_build_flow_output(
            [selected_landmark_0],
            [],
            TestBuildFlowHelper.gripper_domain,
            TestBuildFlowHelper.gripper_problem,
            TestBuildFlowHelper.planner_response_model.plans,
            False,
        )
        self.assertEqual(len(build_forward_flow_output.plans), 2)
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
            "node11",
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
