from __future__ import annotations

import os
from pathlib import Path

from runtime_yolk import Yolk

FIXTURE_PATH = "tests/fixtures/yolk_test"


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
