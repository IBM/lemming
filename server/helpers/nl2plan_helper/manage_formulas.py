from typing import Dict, List

from nl2ltl.declare.base import Template

from helpers.planner_helper.planner_helper_data_types import LTLFormula


def get_formulas_from_matched_formulas(
    utterance: str, matched_formulas: Dict[Template, float]
) -> List[LTLFormula]:
    """
    Make the NL2LTL output consumable for Lemming.

    :param utterance: the user utterance.
    :param matched_formulas: the output formulas from NL2LTL.
    :return: the consumable LTL formulas.
    """
    formulas = []
    for formula, confidence in matched_formulas.items():
        formulas.append(
            LTLFormula(
                user_prompt=utterance,
                formula_name=formula,
                formula_ltl=formula.to_ltlf(),
                formula_ppltl=formula.to_ppltl(),
                description=formula.to_english(),
                confidence=confidence,
            )
        )
    return formulas
