import contextlib
import os
from collections.abc import Generator
from os import PathLike
from pathlib import Path


@contextlib.contextmanager
def cd(path: PathLike) -> Generator:  # pylint: disable=invalid-name
    """Change working directory temporarily."""
    old_path = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(str(old_path))
