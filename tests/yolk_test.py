from __future__ import annotations

from pathlib import Path

from runtime_yolk import ConfigLoader
from runtime_yolk import EnvLoader
from runtime_yolk import Yolk


def test_working_directory_attr_unset() -> None:
    yolk = Yolk()

    assert yolk._working_directory == Path().cwd()


def test_working_directory_attr_set() -> None:
    expected = Path("tests/fixtures")

    yolk = Yolk(working_directory="tests/fixtures")

    assert yolk._working_directory == expected


def test_empty_configloader() -> None:
    yolk = Yolk()

    assert isinstance(yolk._config, ConfigLoader)


def test_empty_envloader() -> None:
    yolk = Yolk()

    assert isinstance(yolk._env, EnvLoader)
