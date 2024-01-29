import unittest
import os
from typing import List
from planners.drivers.planner_driver_datatype import PlanningResult
from helpers.common_helper.file_helper import read_str_from_file
from helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topk,
)
from helpers.planner_helper.planner_helper_data_types import (
    PlanningTask,
    LandmarkCategory,
    Landmark,
    SelectionInfo,
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
    planner_response_model: PlanningResult

    toy_domain: str
    toy_problem: str
    toy_landmarks: List[Landmark]
    toy_planner_response_model: PlanningResult

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
        TestBuildFlowHelper.planner_response_model = get_plan_topk(
            PlanningTask(
                domain=TestBuildFlowHelper.gripper_domain,
                problem=TestBuildFlowHelper.gripper_problem,
                num_plans=6,
                quality_bound=1.0,
            )
        )

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
        TestBuildFlowHelper.toy_planner_response_model = get_plan_topk(
            PlanningTask(
                domain=TestBuildFlowHelper.toy_domain,
                problem=TestBuildFlowHelper.toy_problem,
                num_plans=6,
                quality_bound=1.0,
            )
        )

    def test_get_build_forward_flow_output_no_selection_info_no_landmark(
        self,
    ) -> None:
        build_forward_flow_output, _, _ = get_build_flow_output(
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
        self.assertEqual(
            build_forward_flow_output.choice_infos[0].max_num_plans, 0
        )
        self.assertEqual(
            len(
                build_forward_flow_output.choice_infos[
                    0
                ].action_name_plan_idx_map
            ),
            0,
        )
        self.assertEqual(
            build_forward_flow_output.choice_infos[
                0
            ].nodes_with_multiple_out_edges[0],
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
        build_forward_flow_output, _, _ = get_build_flow_output(
            [],
            [],
            TestBuildFlowHelper.toy_domain,
            TestBuildFlowHelper.toy_problem,
            TestBuildFlowHelper.toy_planner_response_model.plans,
            True,
        )
        self.assertGreater(len(build_forward_flow_output.plans), 0)
        self.assertEqual(len(build_forward_flow_output.choice_infos), 1)
        self.assertIsNone(build_forward_flow_output.choice_infos[0].landmark)
        self.assertEqual(
            build_forward_flow_output.choice_infos[0].max_num_plans, 0
        )
        self.assertEqual(
            len(
                build_forward_flow_output.choice_infos[
                    0
                ].action_name_plan_idx_map
            ),
            0,
        )
        self.assertEqual(
            build_forward_flow_output.choice_infos[
                0
            ].nodes_with_multiple_out_edges[0],
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
        selected_landmark_0 = SelectionInfo(
            selected_first_achiever="",
            selected_plan_hashes=[
                "6a81b2a65657b4444a989205b590c346",
            ],
        )
        build_forward_flow_output, _, _ = get_build_flow_output(
            [selected_landmark_0],
            [],
            TestBuildFlowHelper.gripper_domain,
            TestBuildFlowHelper.gripper_problem,
            TestBuildFlowHelper.planner_response_model.plans,
            True,
        )
        self.assertGreater(len(build_forward_flow_output.plans), 0)
        self.assertEqual(len(build_forward_flow_output.choice_infos), 0)

    def test_get_build_backword_flow_output_no_selection_info_no_landmark(
        self,
    ) -> None:
        build_forward_flow_output, _, _ = get_build_flow_output(
            [],
            [],
            TestBuildFlowHelper.gripper_domain,
            TestBuildFlowHelper.gripper_problem,
            TestBuildFlowHelper.planner_response_model.plans,
            False,
        )
        self.assertGreater(len(build_forward_flow_output.plans), 0)
        self.assertGreater(len(build_forward_flow_output.choice_infos), 0)
        self.assertIsNone(build_forward_flow_output.choice_infos[0].landmark)
        self.assertEqual(len(build_forward_flow_output.networkx_graph), 5)

    def test_get_build_backword_flow_output_one_selection_info_no_landmark(
        self,
    ) -> None:
        selected_landmark_0 = SelectionInfo(
            selected_first_achiever="",
            selected_plan_hashes=[
                "6a81b2a65657b4444a989205b590c346"
            ],
        )
        build_forward_flow_output, _, _ = get_build_flow_output(
            [selected_landmark_0],
            [],
            TestBuildFlowHelper.gripper_domain,
            TestBuildFlowHelper.gripper_problem,
            TestBuildFlowHelper.planner_response_model.plans,
            False,
        )
        self.assertGreater(len(build_forward_flow_output.plans), 0)
        self.assertEqual(len(build_forward_flow_output.choice_infos), 0)
        self.assertEqual(len(build_forward_flow_output.networkx_graph), 5)
