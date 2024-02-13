import unittest

from nl2ltl.declare.declare import Response
from pylogics.syntax.ltl import Atomic

from server.helpers.nl2plan_helper.manage_formulas import (
    get_formulas_from_matched_formulas,
)
from server.helpers.nl2plan_helper.nl2ltl_helper import LTLFormula


class TestNl2Plan(unittest.TestCase):
    def test_matching_formulas(self) -> None:
        matched_formulas = {
            Response(Atomic("hasdonee"), Atomic("hasdoned")): 1.0
        }
        utterance = "Do E before D"
        formulas = get_formulas_from_matched_formulas(
            utterance, matched_formulas
        )
        self.assertEqual(len(formulas), 1)
        for formula in formulas:
            self.assertEqual(type(formula), LTLFormula)
        self.assertEqual(formulas[0].user_prompt, utterance)
