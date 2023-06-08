import unittest
from helpers.common_helper.file_helper import read_str_from_file
from helpers.planner_helper.planner_helper_data_types import (
    LandmarkCategory,
)
from helpers.planner_helper.planner_helper import (
    get_plan_topq,
    get_landmarks_by_landmark_category,
    get_dot_graph_str,
)


class TestPlannerHelper(unittest.TestCase):
    def test_get_plan_topq(self) -> None:
        domain = read_str_from_file("./tests/data/pddl/domain.pddl")
        problem = read_str_from_file("./tests/data/pddl/problem.pddl")
        result = get_plan_topq(domain, problem, 6, 1.0)
        self.assertEqual(len(result.plans), 1)

    def test_get_landmarks_by_landmark_category(self) -> None:
        domain = read_str_from_file("./tests/data/pddl/domain.pddl")
        problem = read_str_from_file("./tests/data/pddl/problem.pddl")
        landmarks = get_landmarks_by_landmark_category(
            domain, problem, LandmarkCategory.RWH
        )
        self.assertEqual(len(landmarks), 4)

    def test_get_dot_graph_str(self) -> None:
        domain = read_str_from_file("./tests/data/pddl/domain.pddl")
        problem = read_str_from_file("./tests/data/pddl/problem.pddl")
        result = get_plan_topq(domain, problem, 6, 1.0)
        dot_graph_str = get_dot_graph_str(domain, problem, result)
        self.assertEqual(len(dot_graph_str), 964)
