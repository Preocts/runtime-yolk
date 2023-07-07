from __future__ import annotations

import os
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest
from runtime_yolk import ConfigLoader

FIXTURE_PATH = Path("tests/fixtures/default_and_env_config")


@pytest.fixture
def config_instance() -> ConfigLoader:
    return ConfigLoader()


@pytest.fixture
def config_prod() -> Generator[ConfigLoader, None, None]:
    with patch.dict(os.environ, {"YOLK_ENVIRONMENT": "prod"}):
        yield ConfigLoader(working_directory=FIXTURE_PATH)


def test_load_with_no_default_config(
    config_instance: ConfigLoader,
) -> None:
    config_instance = ConfigLoader()
    config_instance.load()

    assert config_instance.config.get("DEFAULT", "logging_level") == "WARNING"
    assert config_instance.config.get("DEFAULT", "environment") == ""


def test_load_default_and_env_config(config_prod: ConfigLoader) -> None:
    config_prod.load()

    assert config_prod.config.get("DEFAULT", "logging_level") == "ERROR"
    assert config_prod.config.get("DEFAULT", "environment") == "prod"


@pytest.mark.parametrize(
    ("in_str", "out_str"),
    (
        ("{{ENVIRONMENT}}", "production"),
        ("{{SECOND_VALUE}}", "eggs are cool"),
        ("{{NOT FOUND}}", ""),
        (
            "This{{ENVIRONMENT}}should replace because {{SECOND_VALUE}}",
            "Thisproductionshould replace because eggs are cool",
        ),
        (
            "This {{ENVIRONMENT}} should {{hi}} replace because --{{SECOND_VALUE}}--",
            "This production should  replace because --eggs are cool--",
        ),
    ),
)
def test_interpolate_environment(in_str: str, out_str: str) -> None:
    config = ConfigLoader()
    test_env = {
        "ENVIRONMENT": "production",
        "SECOND_VALUE": "eggs are cool",
    }

    with patch.dict(os.environ, test_env):
        result = config._interpolate_environment(in_str)

    assert result == out_str
