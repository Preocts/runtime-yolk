from __future__ import annotations

import os
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest
from runtime_yolk import config_loader

FIXTURE_PATH = Path("tests/fixtures/default_and_env_config")


@pytest.fixture
def config_instance() -> config_loader.ConfigLoader:
    return config_loader.ConfigLoader()


@pytest.fixture
def config_prod() -> Generator[config_loader.ConfigLoader, None, None]:
    with patch.dict(os.environ, {"ENVIRONMENT": "prod"}):
        yield config_loader.ConfigLoader(working_directory=FIXTURE_PATH)


def test_load_with_no_default_config(
    config_instance: config_loader.ConfigLoader,
) -> None:
    config_instance = config_loader.ConfigLoader()
    config_instance.load()

    loaded_config = config_instance.get_config()

    exp_level = config_loader.DEFAULT_DEFAULT["logging_level"]
    exp_env = config_loader.DEFAULT_DEFAULT["environment"]
    exp_level_key = config_loader.DEFAULT_ENVIROMENT_VARIABLES["logging_level"]
    exp_env_key = config_loader.DEFAULT_ENVIROMENT_VARIABLES["environment"]

    assert loaded_config.get("DEFAULT", "logging_level") == exp_level
    assert loaded_config.get("DEFAULT", "environment") == exp_env
    assert loaded_config.get("ENVIRONMENT_VARIABLES", "logging_level") == exp_level_key
    assert loaded_config.get("ENVIRONMENT_VARIABLES", "environment") == exp_env_key


def test_load_default_and_env_config(config_prod: config_loader.ConfigLoader) -> None:
    config_prod.load()

    loaded_config = config_prod.get_config()

    assert loaded_config.get("DEFAULT", "logging_level") == "ERROR"
    assert loaded_config.get("DEFAULT", "environment") == "prod"


def test_load_default_no_additional(config_prod: config_loader.ConfigLoader) -> None:
    config_prod.load(load_additional=False)

    loaded_config = config_prod.get_config()

    assert loaded_config.get("DEFAULT", "logging_level") != "ERROR"
    assert loaded_config.get("DEFAULT", "environment") != "prod"
