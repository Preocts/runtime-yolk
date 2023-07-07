"""Unit tests for .env file loader"""
from __future__ import annotations

import os
import tempfile
from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest

from runtime_yolk import env_loader


ENV_FILE_CONTENTS = [
    "SECRETBOX_TEST_PROJECT_ENVIRONMENT=sandbox",
    "#What type of .env supports comments?",
    "",
    "BROKEN KEY",
    "VALID==",
    "SUPER_SECRET  =          12345",
    "PASSWORD = correct horse battery staple",
    'USER_NAME="not_admin"',
    "MESSAGE = '    Totally not an \"admin\" account logging in'",
    "  SINGLE_QUOTES = 'test'",
    "export NESTED_QUOTES = \"'Double your quotes, double your fun'\"",
    '   eXport SHELL_COMPATIBLE = "well, that happened"',
]

ENV_FILE_EXPECTED = {
    "SECRETBOX_TEST_PROJECT_ENVIRONMENT": "sandbox",
    "VALID": "=",
    "SUPER_SECRET": "12345",
    "PASSWORD": "correct horse battery staple",
    "USER_NAME": "not_admin",
    "MESSAGE": '    Totally not an "admin" account logging in',
    "SINGLE_QUOTES": "test",
    "NESTED_QUOTES": "'Double your quotes, double your fun'",
    "SHELL_COMPATIBLE": "well, that happened",
}

WD = Path("tests/fixtures")  # Working directory for tests


@pytest.fixture
def mock_env_file() -> Generator[str, None, None]:
    """Builds and returns filename of a mock .env file"""
    try:
        file_desc, path = tempfile.mkstemp(dir=WD)
        filename = Path(path).name
        with os.fdopen(file_desc, "w", encoding="utf-8") as temp_file:
            temp_file.write("\n".join(ENV_FILE_CONTENTS))
        yield filename
    finally:
        os.remove(path)


@pytest.fixture
def loader() -> Generator[env_loader.EnvLoader, None, None]:
    """Create us a fixture"""
    with patch.dict(os.environ, {}):
        loader = env_loader.EnvLoader(working_directory=WD)
        yield loader


def test_load_env_file(mock_env_file: str, loader: env_loader.EnvLoader) -> None:
    """Load and confirm expected values"""
    loader.load(filename=mock_env_file)
    for key, value in ENV_FILE_EXPECTED.items():
        assert os.getenv(key) == value, f"{key}, {value}"


def test_load_missing_file(loader: env_loader.EnvLoader) -> None:
    """Confirm clean run if file is missing"""
    assert not loader.load(filename="BYWHATCHANGEWOULDTHISSEXIST")


@pytest.mark.parametrize(
    ("given", "expected"),
    (
        ("\"'test'\"", "'test'"),
        ("'\"test\"'", '"test"'),
        ("'test'\"", "'test'\""),
        ("\"'test'", "\"'test'"),
        ("'\"test\"'", '"test"'),
        ("\"'test'\"", "'test'"),
        ('"test"\'', '"test"\''),
        ('\'"test"', '\'"test"'),
    ),
)
def test_remove_lt_quotes(
    loader: env_loader.EnvLoader,
    given: str,
    expected: str,
) -> None:
    assert loader._remove_lt_quotes(given) == expected


@pytest.mark.parametrize(
    ("given", "expected"),
    (
        ("EXPoRT \tTest", "Test"),
        ("EXPoRT export", "export"),
    ),
)
def test_strip_export(loader: env_loader.EnvLoader, given: str, expected: str) -> None:
    assert loader._strip_export(given) == expected
