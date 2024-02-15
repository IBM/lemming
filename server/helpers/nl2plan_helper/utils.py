import contextlib
import functools
import sys
import tempfile
from pathlib import Path
from typing import Generator


@contextlib.contextmanager
def temporary_directory() -> Generator[Path, None, None]:
    """
    Create a temporary directory and clean up when done.

    This function is a context manager that creates a temporary directory.
    It wraps tempfile.TemporaryDirectory in order to make the cleanup more
    robust (e.g. managing a PermissionError in Windows:
    https://www.scivision.dev/python-tempfile-permission-error-windows/).
    """
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = Path(temp_dir.name)

    yield temp_path

    # when done with temporary directory
    try:
        temp_dir.cleanup()
    except PermissionError:
        pass


def requires_optional(fn):
    @functools.wraps(fn)
    async def wrapper_decor(*args, **kwargs):
        if "nl2ltl" not in sys.modules:
            raise ModuleNotFoundError(
                f"NL2LTL is required to instantiate {fn.__name__}"
            )
        return await fn(*args, **kwargs)

    return wrapper_decor
