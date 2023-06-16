from typing import Dict, Tuple

from helpers.planner_helper.planner_helper_data_types import (LTLFormula,
                                                              ToolCompiler)
from pddl.core import Domain, Problem
from pddl.logic import Predicate
from plan4past.compiler import Compiler
from pylogics.syntax.base import Formula
from pylogics.syntax.pltl import Atomic


def compile_instance(
    domain: Domain,
    problem: Problem,
    formula: Formula,
    tool: ToolCompiler,
    mapping: Dict[Atomic, Predicate] = None,
) -> Tuple[Domain, Problem]:
    """Compile the PDDL domain and problem files and the LTL/PPLTL goal formula."""
    compiled_domain, compiled_problem = Domain("empty"), Problem("empty")
    if tool == ToolCompiler.P4P:
        compiler = Compiler(domain, problem, formula, mapping)
        compiler.compile()
        compiled_domain, compiled_problem = compiler.result
    else:
        assert tool == ToolCompiler.LF2F, "Invalid planning compiler."
        # TODO: add compilation for LF2F
    return compiled_domain, compiled_problem


def get_goal_formula(formula: LTLFormula, tool: ToolCompiler) -> Formula:
    """Get the goal formula from the NL2LTL output."""
    if tool == ToolCompiler.P4P:
        return formula.formula_ppltl
    else:
        return formula.formula_ltl
