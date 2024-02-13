import unittest
from server.simulator.simulation_datatypes import (
    SimulationResultUnit,
    SimulationOutput,
    SimulationInput,
)
from server.helpers.planner_helper.planner_helper_data_types import (
    PlanningTask,
)


class TestSimulationDatatype(unittest.TestCase):
    def test_get_simulation_metrics(self) -> None:
        simulation_results = [
            [
                SimulationResultUnit(
                    chosen_edge="a",
                    is_edge_selected=True,
                    num_remaining_plans=3,
                    is_from_landmark=True,
                    is_disambiguation_done=False,
                ),
                SimulationResultUnit(
                    chosen_edge="b",
                    is_edge_selected=True,
                    num_remaining_plans=3,
                    is_from_landmark=False,
                    is_disambiguation_done=False,
                ),
                SimulationResultUnit(
                    chosen_edge="c",
                    is_edge_selected=True,
                    num_remaining_plans=2,
                    is_from_landmark=False,
                    is_disambiguation_done=True,
                ),
                SimulationResultUnit(
                    chosen_edge=None,
                    is_edge_selected=True,
                    num_remaining_plans=2,
                    is_from_landmark=False,
                    is_disambiguation_done=True,
                ),
            ],
            [
                SimulationResultUnit(
                    chosen_edge="a",
                    is_edge_selected=True,
                    num_remaining_plans=3,
                    is_from_landmark=True,
                    is_disambiguation_done=False,
                ),
                SimulationResultUnit(
                    chosen_edge="b",
                    is_edge_selected=True,
                    num_remaining_plans=3,
                    is_from_landmark=False,
                    is_disambiguation_done=False,
                ),
                SimulationResultUnit(
                    chosen_edge="c",
                    is_edge_selected=True,
                    num_remaining_plans=2,
                    is_from_landmark=False,
                    is_disambiguation_done=True,
                ),
                SimulationResultUnit(
                    chosen_edge="d",
                    is_edge_selected=True,
                    num_remaining_plans=2,
                    is_from_landmark=False,
                    is_disambiguation_done=False,
                ),
            ],
        ]
        simulation_output = SimulationOutput(
            simulation_results=simulation_results,
            simulation_input=SimulationInput(
                planning_task=PlanningTask(domain="s", problem="s")
            ),
        )
        metrics = simulation_output.get_simulation_metrics()

        self.assertEqual(len(metrics), len(simulation_results))
        self.assertTrue(metrics[0].is_disambiguation_done)
        self.assertEqual(metrics[0].num_edges_chosen, 3)
        self.assertEqual(metrics[0].num_landmarks_chosen, 1)
        self.assertFalse(metrics[1].is_disambiguation_done)
        self.assertEqual(metrics[1].num_edges_chosen, 4)
        self.assertEqual(metrics[1].num_landmarks_chosen, 1)
