import os
import unittest
from helpers.common_helper.file_helper import read_str_from_file
from helpers.planner_helper.planner_helper_data_types import (
    PlanningTask,
    PlanDisambiguationView,
    LandmarkCategory,
)
from simulator.simulation_runner import run_simulation
my_dir = os.path.dirname(__file__)
rel_pddl_path = "../data/pddl/{}.pddl"


class TestSimulationRunner(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        TestSimulationRunner.toy_domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("toy/domain"))
        )
        TestSimulationRunner.toy_problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("toy/problem"))
        )

    def test_run_simulation_select_flow(self):
        landmark_category = LandmarkCategory.RWH
        planning_task = PlanningTask(
            domain=TestSimulationRunner.toy_domain,
            problem=TestSimulationRunner.toy_problem,
            num_plans=4,
            quality_bound=20.0,
            timeout=None,
            case_sensitive=False,
            action_name_prefix_preserve=None
        )
        num_replicates = 2
        metrics = run_simulation(
            landmark_category=landmark_category,
            planning_task=planning_task,
            plan_disambiguator_view=PlanDisambiguationView.SELECT,
            use_landmark_to_select_edge=True,
            num_replicates=num_replicates
        )

        self.assertEqual(len(metrics), num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_build_forward_flow(self):
        landmark_category = LandmarkCategory.RWH
        planning_task = PlanningTask(
            domain=TestSimulationRunner.toy_domain,
            problem=TestSimulationRunner.toy_problem,
            num_plans=4,
            quality_bound=20.0,
            timeout=None,
            case_sensitive=False,
            action_name_prefix_preserve=None
        )
        num_replicates = 2
        metrics = run_simulation(
            landmark_category=landmark_category,
            planning_task=planning_task,
            plan_disambiguator_view=PlanDisambiguationView.BUILD_FORWARD,
            use_landmark_to_select_edge=False,
            num_replicates=num_replicates
        )

        self.assertEqual(len(metrics), num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    # @unittest.skip("Build Backward flow needs to be fixed")
    def test_run_simulation_build_backward_flow(self):
        landmark_category = LandmarkCategory.RWH
        planning_task = PlanningTask(
            domain=TestSimulationRunner.toy_domain,
            problem=TestSimulationRunner.toy_problem,
            num_plans=4,
            quality_bound=20.0,
            timeout=None,
            case_sensitive=False,
            action_name_prefix_preserve=None
        )
        num_replicates = 1
        metrics = run_simulation(
            landmark_category=landmark_category,
            planning_task=planning_task,
            plan_disambiguator_view=PlanDisambiguationView.BUILD_BACKWARD,
            use_landmark_to_select_edge=False,
            num_replicates=num_replicates
        )

        self.assertEqual(len(metrics), num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)
