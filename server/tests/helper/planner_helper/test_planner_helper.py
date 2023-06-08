import unittest
import os

from helpers.common_helper.file_helper import read_str_from_file
from helpers.planner_helper.planner_helper_data_types import (
    LandmarkCategory,
    PlanningTask,
)
from helpers.planner_helper.planner_helper import (
    get_plan_topq,
    get_landmarks_by_landmark_category,
    get_dot_graph_str,
)

my_dir = os.path.dirname(__file__)
rel_pddl_path = "../../data/pddl/{}.pddl"


class TestPlannerHelper(unittest.TestCase):
    def test_get_plan_topq(self) -> None:
        domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("domain"))
        )
        problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("problem"))
        )
        result = get_plan_topq(
            PlanningTask(
                domain=domain, problem=problem, num_plans=6, quality_bound=1.0
            )
        )
        self.assertEqual(len(result.plans), 1)

    def test_get_landmarks_by_landmark_category(self) -> None:
        domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("domain"))
        )
        problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("problem"))
        )
        landmarks = get_landmarks_by_landmark_category(
            PlanningTask(domain=domain, problem=problem),
            LandmarkCategory.RWH.value,
        )
        self.assertEqual(len(landmarks), 4)

    def test_get_dot_graph_str(self) -> None:
        domain = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("domain"))
        )
        problem = read_str_from_file(
            os.path.join(my_dir, rel_pddl_path.format("problem"))
        )

        planning_task = PlanningTask(
            domain=domain, problem=problem, num_plans=6, quality_bound=1.0
        )

        result = get_plan_topq(planning_task)
        dot_graph_str = get_dot_graph_str(planning_task, result)
        self.assertEqual(len(dot_graph_str), 964)
