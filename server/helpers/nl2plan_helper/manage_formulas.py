from typing import Dict, List

from helpers.planner_helper.planner_helper_data_types import LTLFormula
from pylogics.syntax.base import Formula


def get_formulas_from_matched_formulas(
    utterance: str, matched_formulas: Dict[Formula, float]
) -> List[LTLFormula]:
    """
    Make the NL2LTL output consumable for Lemming.

    :param matched_formulas: the output formulas from NL2LTL.
    :return: the consumable LTL formulas.
    """
    formulas = []
    for formula, confidence in matched_formulas.items():
        formulas.append(
            LTLFormula(
                user_prompt=utterance,
                formula_name=formula,
                formula_ltl=formula.to_ltl(),
                formula_ppltl=formula.to_ppltl(),
                description=formula.to_english(),
                confidence=confidence,
            )
        )
    return formulas
