from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from _pytest.logging import LogCaptureFixture
from runtime_yolk import Yolk

FIXTURE_PATH = "tests/fixtures/yolk_test"


@pytest.fixture
def temp_file() -> Generator[str, None, None]:
    """Creates a temp file."""
    try:
        file_desc, path = tempfile.mkstemp(prefix="temp_", dir="tests")
        os.close(file_desc)
        yield path
    finally:
        os.remove(path)


def test_working_directory_attr_unset() -> None:
    yolk = Yolk()

    assert yolk._working_directory == Path().cwd()


def test_working_directory_attr_set() -> None:
    expected = Path("tests/fixtures")

    yolk = Yolk(working_directory="tests/fixtures")

    assert yolk._working_directory == expected


def test_config_property_default() -> None:
    yolk = Yolk()

    assert not yolk.config.get("DEFAULT", "environment")


def test_config_load_default_ini() -> None:
    yolk = Yolk(working_directory=FIXTURE_PATH)

    yolk.load_config()

    assert yolk.config.get("DEFAULT", "yolk_test") == "pass"


def test_config_load_with_auto_load_true() -> None:
    yolk = Yolk(working_directory=FIXTURE_PATH, auto_load=True)

    assert yolk.config.get("DEFAULT", "yolk_test") == "pass"


def test_config_load_specific_ini() -> None:
    yolk = Yolk(working_directory=FIXTURE_PATH)

    yolk.load_config("not-application")

    assert yolk.config.get("DEFAULT", "yolk_test") == "eggshell"


def test_config_layers_correctly() -> None:
    yolk = Yolk(working_directory=FIXTURE_PATH)

    yolk.load_config()
    yolk.load_config("not-application")

    assert yolk.config.get("DEFAULT", "yolk_test") == "eggshell"


def test_env_load() -> None:
    yolk = Yolk(working_directory=FIXTURE_PATH)

    yolk.load_env()

    assert os.environ["ENVIRONMENT"] == "test"


def test_env_load_specific_file() -> None:
    yolk = Yolk(working_directory=FIXTURE_PATH)

    yolk.load_env(".env-prod")

    assert os.environ["ENVIRONMENT"] == "prod"


def test_env_load_auto_load() -> None:
    Yolk(working_directory=FIXTURE_PATH, auto_load=True)

    assert os.environ["ENVIRONMENT"] == "test"


@pytest.mark.parametrize(
    ("level", "expected_level"),
    (
        ("DEBUG", 10),
        ("INFO", 20),
        ("WARNING", 30),
        ("ERROR", 40),
        ("CRITICAL", 50),
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
    ),
)
def test_add_logging_impacts_root_logger(
    level: str | int,
    expected_level: int,
    caplog: LogCaptureFixture,
) -> None:
    yolk = Yolk()
    yolk.add_logging(level)
    logger_name = f"test_{level}"
    log = logging.getLogger(logger_name)
    expected_range = list(range(expected_level, 60, 10))

    log.debug("Test")
    log.info("Test")
    log.warning("Test")
    log.error("Test")
    log.critical("Test")

    for name, logl, _ in caplog.record_tuples:
        assert name == logger_name
        assert logl in expected_range

    assert len(caplog.record_tuples) == len(expected_range)
    assert logging.getLogger().level == expected_level


@pytest.mark.parametrize(
    ("name", "expected"),
    (
        (__name__, __name__),
        ("my_logger", "my_logger"),
        (None, "root"),
    ),
)
def test_get_logger(name: str, expected: str) -> None:
    logger = Yolk().get_logger(name)

    assert logger.name == expected


def test_add_logging_file(temp_file: str) -> None:
    yolk = Yolk(auto_load=True)
    log = logging.getLogger("test_log")

    yolk.add_logging_file(temp_file, "CRITICAL")
    log.critical("Testing file writing")
    log.debug("Should not be shown")

    with open(temp_file) as test_in:
        results = test_in.read()

    assert "Testing file writing" in results
    assert "Should not be shown" not in results
