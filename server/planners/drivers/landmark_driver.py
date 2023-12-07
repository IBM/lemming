from pathlib import Path
from typing import List, Optional
import json
import forbiditerative
import tempfile
import subprocess
import sys

from planners.drivers.landmark_driver_datatype import Landmark

build_dir = Path(forbiditerative.__file__).parent / "builds" / "release" / "bin"


def parse_landmarks(result: Path) -> List[Landmark]:
    data = json.loads(result.read_text())
    return [
        Landmark(
            facts=landmark["facts"],
            disjunctive=eval(landmark["disjunctive"]),
            first_achievers=landmark["first_achievers"],
        )
        for landmark in data["landmarks"]
    ]


def get_landmarks(
    category: str,
    domain: str,
    problem: str,
    case_sensitive: Optional[bool] = False,
) -> List[Landmark]:
    """Execute the planner on the task, no search."""
    # a mapping from category to aliases recognized by the planner
    # each alias represents a large amount of settings.
    with tempfile.NamedTemporaryFile() as domain_temp, tempfile.NamedTemporaryFile() as problem_temp:
        # We have to read and write to files because the planner is CLI oriented.
        landmarks_file = Path(tempfile.gettempdir()) / "landmarks.json"
        domain_file = Path(tempfile.gettempdir()) / domain_temp.name
        problem_file = Path(tempfile.gettempdir()) / problem_temp.name
        domain_file.write_text(domain)
        problem_file.write_text(problem)
        translator_options = (
            ["--translate-options", "--case-sensitive", "--search-options"]
            if case_sensitive
            else []
        )
        subprocess.run(
            [sys.executable, "-B", "-m", "driver.main"]
            + ["--build", str(build_dir.absolute())]
            + ["--alias", f"get_landmarks_{category}"]
            + [str(domain_file.absolute()), str(problem_file.absolute())]
            + translator_options,
            cwd=Path(tempfile.gettempdir()),
        )
        return parse_landmarks(landmarks_file)
