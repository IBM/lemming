import os
import unittest
from pathlib import Path

from server.helpers.common_helper.file_helper import (
    read_str_from_file,
    get_model_from_file,
)
from server.helpers.planner_helper.planner_helper_data_types import (
    PlanDisambiguationView,
    LandmarkCategory,
    PlanningTask,
)
from server.simulator.simulation_runner import (
    run_simulation,
    run_simulation_unit,
)
from server.simulator.simulation_datatypes import (
    SimulationInput,
    SimulationOutput,
    SimulationMestricUnits,
    EdgeSelectionType,
)

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
            action_name_prefix_preserve=None,
        )

    def test_run_simulation_select_flow(self):
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.SELECT,
            landmark_category=LandmarkCategory.RWH,
            edge_selection_type=EdgeSelectionType.LANDMARK,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task,
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)
            for simulation_unit in metrics[i]:
                self.assertIsNotNone(simulation_unit.num_actions)
                self.assertIsNotNone(simulation_unit.num_edges)
                self.assertIsNotNone(simulation_unit.num_nodes)
                self.assertGreater(simulation_unit.num_remaining_plans, 0)
                self.assertIsNotNone(simulation_unit.plan_costs)
                self.assertIsNotNone(simulation_unit.num_choice_infos)

    def test_run_simulation_select_flow_greedy_disjunctive_action_landmark_selection(self):
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.SELECT,
            landmark_category=LandmarkCategory.RWH,
            edge_selection_type=EdgeSelectionType.LANDMARK_GREEDY,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task,
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_select_flow_random(self) -> None:
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.SELECT,
            landmark_category=LandmarkCategory.RWH,
            edge_selection_type=EdgeSelectionType.RANDOM,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task,
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_build_forward_flow(self) -> None:
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.BUILD_FORWARD,
            landmark_category=LandmarkCategory.RWH,
            edge_selection_type=EdgeSelectionType.CHOICE_INFO,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task,
        )
        simulation_output = run_simulation(simulation_input)

        metrics = simulation_output.simulation_results
        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_build_forward_flow_random(self) -> None:
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.BUILD_FORWARD,
            landmark_category=LandmarkCategory.RWH,
            edge_selection_type=EdgeSelectionType.RANDOM,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task,
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_build_backward_flow(self) -> None:
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.BUILD_BACKWARD,
            landmark_category=LandmarkCategory.RWH,
            edge_selection_type=EdgeSelectionType.CHOICE_INFO,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task,
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_build_backward_random(self) -> None:
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.BUILD_BACKWARD,
            landmark_category=LandmarkCategory.RWH,
            edge_selection_type=EdgeSelectionType.RANDOM,
            num_replicates=2,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task,
        )
        simulation_output = run_simulation(simulation_input)
        metrics = simulation_output.simulation_results

        self.assertEqual(len(metrics), simulation_input.num_replicates)
        for i in range(len(metrics)):
            self.assertGreaterEqual(len(metrics[i]), 1)

    def test_run_simulation_unit(self) -> None:
        num_replicates = 2
        simulation_input = SimulationInput(
            plan_disambiguator_view=PlanDisambiguationView.SELECT,
            landmark_category=LandmarkCategory.RWH,
            edge_selection_type=EdgeSelectionType.LANDMARK,
            num_replicates=num_replicates,
            setting_name="test",
            planning_task=TestSimulationRunner.planning_task,
        )
        raw_output_file_path, metrics_file_path = run_simulation_unit(
            simulation_input
        )
        # file read
        simulation_output = get_model_from_file(
            Path(raw_output_file_path), SimulationOutput
        )
        simulation_metrics = get_model_from_file(
            Path(metrics_file_path), SimulationMestricUnits
        )

        self.assertIsNotNone(simulation_output)
        self.assertEqual(
            len(simulation_metrics.simulation_metrics_units), num_replicates
        )
