from typing import List

import unittest
import os

from planners.drivers.planner_driver_datatype import PlanningResult
from helpers.common_helper.file_helper import read_str_from_file
from helpers.planner_helper.planner_helper import (
    get_landmarks_by_landmark_category,
    get_plan_topk,
)
from helpers.planner_helper.planner_helper_data_types import (
    LandmarkCategory,
    SelectionInfo,
    PlanningTask,
    Landmark,
    SelectionPriority,
)
from helpers.plan_disambiguator_helper.selection_flow_helper import (
    get_selection_flow_output,
)

my_dir = os.path.dirname(__file__)
rel_pddl_path = "../../data/pddl/{}.pddl"


class TestSelectionFlowHelper(unittest.TestCase):
    gripper_domain: str
    gripper_problem: str
    gripper_landmarks: List[Landmark]
    planner_response_model: PlanningResult

    travel_domain: str
    travel_problem: str
    travel_landmarks: List[Landmark]
    travel_planner_response_model: PlanningResult

    toy_domain: str
    toy_problem: str
    toy_landmarks: List[Landmark]
    toy_planner_response_model: PlanningResult

    @classmethod
    def setUpClass(cls) -> None:
        TestSelectionFlowHelper.toy_domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("toy/domain"))
        )
        TestSelectionFlowHelper.toy_problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("toy/problem"))
        )
        TestSelectionFlowHelper.toy_landmarks = (
            get_landmarks_by_landmark_category(
                PlanningTask(
                    domain=TestSelectionFlowHelper.toy_domain,
                    problem=TestSelectionFlowHelper.toy_problem,
                ),
                LandmarkCategory.RWH.value,
            )
        )
        TestSelectionFlowHelper.toy_planner_response_model = get_plan_topk(
            PlanningTask(
                domain=TestSelectionFlowHelper.toy_domain,
                problem=TestSelectionFlowHelper.toy_problem,
                num_plans=10,
                quality_bound=1.2,
            )
        )

        TestSelectionFlowHelper.gripper_domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("gripper/domain"))
        )
        TestSelectionFlowHelper.gripper_problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("gripper/problem"))
        )
        TestSelectionFlowHelper.gripper_landmarks = (
            get_landmarks_by_landmark_category(
                PlanningTask(
                    domain=TestSelectionFlowHelper.gripper_domain,
                    problem=TestSelectionFlowHelper.gripper_problem,
                ),
                LandmarkCategory.RWH.value,
            )
        )
        TestSelectionFlowHelper.planner_response_model = get_plan_topk(
            PlanningTask(
                domain=TestSelectionFlowHelper.gripper_domain,
                problem=TestSelectionFlowHelper.gripper_problem,
                num_plans=10,
                quality_bound=1.2,
            )
        )

        TestSelectionFlowHelper.travel_domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("travel/domain"))
        )
        TestSelectionFlowHelper.travel_problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("travel/problem"))
        )
        TestSelectionFlowHelper.travel_landmarks = (
            get_landmarks_by_landmark_category(
                PlanningTask(
                    domain=TestSelectionFlowHelper.travel_domain,
                    problem=TestSelectionFlowHelper.travel_problem,
                ),
                LandmarkCategory.RWH.value,
            )
        )
        TestSelectionFlowHelper.travel_planner_response_model = get_plan_topk(
            PlanningTask(
                domain=TestSelectionFlowHelper.travel_domain,
                problem=TestSelectionFlowHelper.travel_problem,
                num_plans=10,
                quality_bound=1.2,
            )
        )

    def test_get_selection_flow_output_no_selected_landmarks(self) -> None:
        selected_landmark_0 = SelectionInfo(
            selected_first_achiever="pick ball2 rooma right",
            selected_plan_hashes=[
                "6a81b2a65657b4444a989205b590c346",
                "b458359fe5af1ceb47b53d23ebb4d635",
            ],
        )
        selection_flow_output, _, _ = get_selection_flow_output(
            [selected_landmark_0],
            TestSelectionFlowHelper.gripper_landmarks,
            TestSelectionFlowHelper.gripper_domain,
            TestSelectionFlowHelper.gripper_problem,
            TestSelectionFlowHelper.planner_response_model.plans,
            SelectionPriority.MAX_PLANS.value,
        )
        self.assertGreater(len(selection_flow_output.plans), 0)
        self.assertGreater(len(selection_flow_output.choice_infos), 0)
        self.assertEqual(len(selection_flow_output.networkx_graph), 5)

    def test_get_selection_flow_output_no_selected_landmarks_gripper(
        self,
    ) -> None:
        selected_landmark_0 = SelectionInfo(
            selected_first_achiever="",
            selected_plan_hashes=[],
        )
        selection_flow_output, _, _ = get_selection_flow_output(
            [selected_landmark_0],
            TestSelectionFlowHelper.gripper_landmarks,
            TestSelectionFlowHelper.gripper_domain,
            TestSelectionFlowHelper.gripper_problem,
            TestSelectionFlowHelper.planner_response_model.plans,
            SelectionPriority.MAX_PLANS.value,
        )
        self.assertGreater(len(selection_flow_output.plans), 0)
        self.assertGreater(len(selection_flow_output.choice_infos), 0)
        self.assertEqual(len(selection_flow_output.networkx_graph), 5)

    def test_get_selection_flow_output_no_selected_landmarks_travel(
        self,
    ) -> None:
        selected_landmark_0 = SelectionInfo(
            selected_first_achiever="",
            selected_plan_hashes=[],
        )
        selection_flow_output, _, _ = get_selection_flow_output(
            [selected_landmark_0],
            TestSelectionFlowHelper.travel_landmarks,
            TestSelectionFlowHelper.travel_domain,
            TestSelectionFlowHelper.travel_problem,
            TestSelectionFlowHelper.travel_planner_response_model.plans,
            SelectionPriority.MAX_PLANS.value,
        )
        self.assertGreater(len(selection_flow_output.plans), 0)
        self.assertGreater(len(selection_flow_output.choice_infos), 0)
        self.assertEqual(len(selection_flow_output.networkx_graph), 5)

    def test_get_selection_flow_output_no_landmarks_no_selection_info(
        self,
    ) -> None:
        selection_flow_output, _, _ = get_selection_flow_output(
            [],
            [],
            TestSelectionFlowHelper.gripper_domain,
            TestSelectionFlowHelper.gripper_problem,
            TestSelectionFlowHelper.planner_response_model.plans,
            SelectionPriority.MAX_PLANS.value,
        )
        self.assertGreater(len(selection_flow_output.plans), 0)
        self.assertGreater(len(selection_flow_output.choice_infos), 0)
        self.assertEqual(len(selection_flow_output.networkx_graph), 5)
