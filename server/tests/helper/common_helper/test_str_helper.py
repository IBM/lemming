import unittest
from typing import List

from server.helpers.common_helper.str_helper import format_plan


class TestStrHelper(unittest.TestCase):
    def test_format_plan(self) -> None:
        plan: List[str] = list()
        plan.append("a   ")
        plan.append("b c d ")
        res = format_plan(plan)
        self.assertEqual(res, ["a", "b c d"])
