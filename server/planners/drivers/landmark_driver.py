from pathlib import Path
from typing import List
import tempfile

from forbiditerative import planners
from server.planners.drivers.landmark_driver_datatype import Landmark
from server.helpers.planner_helper.planner_helper_data_types import (
    LandmarkCategory,
)


def get_landmarks(
    category: str,
    domain: str,
    problem: str,
) -> List[Landmark]:
    if category != LandmarkCategory.RWH.value:
        raise NotImplementedError

    with (
        tempfile.NamedTemporaryFile() as domain_temp,
        tempfile.NamedTemporaryFile() as problem_temp,
    ):
        domain_file = Path(tempfile.gettempdir()) / domain_temp.name
        problem_file = Path(tempfile.gettempdir()) / problem_temp.name
        domain_file.write_text(domain)
        problem_file.write_text(problem)

        result = planners.get_landmarks(
            domain_file=domain_file, problem_file=problem_file
        )
        return [
            Landmark(
                facts=landmark["facts"],
                disjunctive=landmark["disjunctive"] == "True",
                first_achievers=landmark["first_achievers"],
            )
            for landmark in result["landmarks"]
        ]
