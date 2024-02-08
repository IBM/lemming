from typing import Dict, List, Optional, Tuple

from pylogics.parsers import parse_pltl

from server.helpers.planner_helper.planner_helper_data_types import (
    LTLFormula,
    ToolCompiler,
)
from pddl.core import Domain, Problem
from pddl.logic import Predicate
from plan4past.compiler import Compiler
from pylogics.syntax.base import Formula, And
from pylogics.syntax.pltl import Atomic


def compile_instance(
    domain: Domain,
    problem: Problem,
    formula: Formula,
    tool: ToolCompiler,
    mapping: Optional[Dict[Atomic, Predicate]] = None,
) -> Tuple[Domain, Problem]:
    """Compile the PDDL domain and problem files and the LTL/PPLTL goal
    formula."""
    compiled_domain, compiled_problem = Domain("empty"), Problem(
        "p-empty", domain_name="empty"
    )
    if tool == ToolCompiler.P4P:
        compiler = Compiler(domain, problem, formula, mapping)
        compiler.compile()
        compiled_domain, compiled_problem = compiler.result
    elif tool == ToolCompiler.LF2F:
        # TODO: add compilation for LF2F
        assert tool == ToolCompiler.LF2F, "Invalid planning compiler."
    return compiled_domain, compiled_problem


def get_goal_formula(
    formulas: List[LTLFormula], reachability_goal: Formula, tool: ToolCompiler
) -> Formula:
    """Get the goal formula from the list of formulas."""
    if tool == ToolCompiler.P4P:
        if isinstance(reachability_goal, And):
            reachability_formula = (
                f"O({' & '.join(str(op) for op in reachability_goal.operands)})"
            )
        else:
            reachability_formula = f"O({reachability_goal})"
        constraints_formula = " & ".join(
            [f"({formula.formula_ppltl})" for formula in formulas]
        )
        return parse_pltl(f"({reachability_formula}) & {constraints_formula}")
    assert tool == ToolCompiler.LF2F, "Invalid planning compiler."
    # TODO: remove pylogics strong next X[!] for LF2F
    return And()
