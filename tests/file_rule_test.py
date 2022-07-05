from __future__ import annotations

import pytest
from runtime_yolk.util import file_rule


@pytest.mark.parametrize(
    ("filename", "environment", "expected"),
    (
        ("test", "", "test.ini"),
        ("test", "dev", "test-dev.ini"),
        ("test", "DEV", "test-dev.ini"),
        (" TEST ", " dev ", "test-dev.ini"),
        ("test file", "dev\tenv", "test_file-dev_env.ini"),
    ),
)
def test_file_rule(filename: str, environment: str, expected: str) -> None:
    assert file_rule.get_file_name(filename, environment) == expected
