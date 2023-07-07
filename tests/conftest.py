from __future__ import annotations

import os
import tempfile
from collections.abc import Generator

import pytest


@pytest.fixture
def temp_file() -> Generator[tuple[int, str], None, None]:
    """Yields file_descriptor and path"""
    try:
        file_desc, path = tempfile.mkstemp(prefix="temp_", dir="tests")
        os.close(file_desc)
        yield file_desc, path
    finally:
        os.remove(path)
