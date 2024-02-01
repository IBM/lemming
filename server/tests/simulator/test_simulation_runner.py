import os
import unittest
from helpers.common_helper.file_helper import (
    read_str_from_file, create_file_from_base_model, get_model_from_file)
from helpers.planner_helper.planner_helper_data_types import (
    PlanDisambiguationView,
    LandmarkCategory,
    PlanningTask,
)
from simulator.simulation_runner import run_simulation
from simulator.simulation_datatypes import (SimulationInput, SimulationOutput)

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
        TestSimulationRunner.planning_task = PlanningTask(
            domain=TestSimulationRunner.toy_domain,
            problem=TestSimulationRunner.toy_problem,
            num_plans=4,
            quality_bound=20.0,
            timeout=None,
            case_sensitive=False,
            action_name_prefix_preserve=None
        )

    def test_run_simulation_select_flow(self):
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.SELECT,
            landmark_category=LandmarkCategory.RWH,
            select_edge_randomly=False,
            use_landmark_to_select_edge=True,
            use_greedy_disjunctive_action_selection=False,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_select_flow_greedy_disjunctive_action_landmark_selection(self):
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.SELECT,
            landmark_category=LandmarkCategory.RWH,
            select_edge_randomly=False,
            use_landmark_to_select_edge=True,
            use_greedy_disjunctive_action_selection=True,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_select_flow_random(self):
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.SELECT,
            landmark_category=LandmarkCategory.RWH,
            select_edge_randomly=True,
            use_landmark_to_select_edge=True,
            use_greedy_disjunctive_action_selection=False,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_build_forward_flow(self):
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.BUILD_FORWARD,
            landmark_category=LandmarkCategory.RWH,
            select_edge_randomly=False,
            use_landmark_to_select_edge=False,
            use_greedy_disjunctive_action_selection=False,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task
        )
        simulation_output = run_simulation(simulation_input)

        metrics = simulation_output.simulation_results
        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_build_forward_flow_random(self):
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.BUILD_FORWARD,
            landmark_category=LandmarkCategory.RWH,
            select_edge_randomly=True,
            use_landmark_to_select_edge=False,
            use_greedy_disjunctive_action_selection=False,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_build_backward_flow(self):
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.BUILD_BACKWARD,
            landmark_category=LandmarkCategory.RWH,
            select_edge_randomly=False,
            use_landmark_to_select_edge=False,
            use_greedy_disjunctive_action_selection=False,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_build_backward_random(self):
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.BUILD_BACKWARD,
            landmark_category=LandmarkCategory.RWH,
            select_edge_randomly=True,
            use_landmark_to_select_edge=False,
            use_greedy_disjunctive_action_selection=False,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_select_flow_file_ops(self):
        num_replicates = 2
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.SELECT,
            landmark_category=LandmarkCategory.RWH,
            select_edge_randomly=False,
            use_landmark_to_select_edge=True,
            use_greedy_disjunctive_action_selection=False,
            num_replicates=num_replicates,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.get_simulation_metrics()

        # file write
        file_path = "sample_output.txt"
        create_file_from_base_model(file_path, simulation_output)
        # file read
        simulation_output = get_model_from_file(file_path, SimulationOutput)

        self.assertIsNotNone(simulation_output)
        self.assertEqual(len(metrics), num_replicates)
