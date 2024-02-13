import contextlib
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
