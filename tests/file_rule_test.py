from __future__ import annotations

import pytest
from runtime_yolk.util import file_rule


@pytest.mark.parametrize(
    ("filename", "environment", "expected"),
    (
        ("test.ini", "", "test.ini"),
        ("test.ini", "dev", "test_dev.ini"),
        ("test", "DEV", "test_dev"),
        (" TEST.INI ", " dev ", "test_dev.ini"),
        ("test file.ini", "dev\tenv", "test_file_dev_env.ini"),
    ),
)
def test_file_rule(filename: str, environment: str, expected: str) -> None:
    assert file_rule.get_file_name(filename, environment) == expected
