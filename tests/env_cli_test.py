from __future__ import annotations

from pathlib import Path

import pytest
from runtime_yolk import env_cli

FIXTURE_ENV = "tests/fixtures/env_cli_test/.env"
EXPECTED_CONTENTS = Path(FIXTURE_ENV).read_text()


def test_parse_args() -> None:
    cli_args = ["test_key", "test_value", "-F", "tests/fixtures/env_cli_test/.env"]

    args = env_cli._parse_args(cli_args)

    assert args.key == "test_key"
    assert args.value == "test_value"
    assert args.update is not True
    assert args.file == "tests/fixtures/env_cli_test/.env"


def test_parse_args_update() -> None:
    cli_args = ["test_key", "test_value", "--update"]
    cli_flag = ["test_key", "test_value", "-U"]

    args = env_cli._parse_args(cli_args)
    args_flags = env_cli._parse_args(cli_flag)

    assert args.update is True
    assert args_flags.update is True
    assert args.file == ".env"


def test_parse_args_delete() -> None:
    cli_args = ["test_key", "--delete"]
    cli_flag = ["test_key", "-D"]

    args = env_cli._parse_args(cli_args)
    args_flags = env_cli._parse_args(cli_flag)

    assert args.delete is True
    assert args_flags.delete is True


@pytest.mark.parametrize(
    ("file_", "expected"),
    (
        (FIXTURE_ENV, EXPECTED_CONTENTS),
        (".missingno", ""),
    ),
)
def test_read_file(file_: str, expected: str) -> None:
    assert env_cli._read_file(file_) == expected


def test_save_file(temp_file: tuple[int, str]) -> None:
    _, filename = temp_file

    env_cli._save_file(filename, EXPECTED_CONTENTS)

    contents = Path(filename).read_text()

    assert contents == EXPECTED_CONTENTS


def test_add_key() -> None:
    expected_lines = EXPECTED_CONTENTS.split("\n")
    expected_lines.append("NEWVALUE=testing")
    expected = "\n".join(expected_lines)

    results = env_cli._add_key("newvalue", "testing", EXPECTED_CONTENTS)

    assert results == expected


def test_contains_key() -> None:
    assert env_cli._contains_key("TEST1", EXPECTED_CONTENTS)
    assert env_cli._contains_key("TEST2", EXPECTED_CONTENTS)
    assert not env_cli._contains_key("TEST3", EXPECTED_CONTENTS)
