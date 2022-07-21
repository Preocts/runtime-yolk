from __future__ import annotations

from pathlib import Path

import pytest
from runtime_yolk import env_cli

FIXTURE_ENV = "tests/fixtures/env_cli_test/.env"
EXPECTED_CONTENTS = Path(FIXTURE_ENV).read_text()


@pytest.fixture
def temp_env(temp_file: tuple[int, str]) -> str:
    """Create temp env populated with fixture contents."""
    with open(temp_file[1], "w") as tempfile:
        tempfile.write(EXPECTED_CONTENTS)
    return temp_file[1]


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

    env_cli._write_file(filename, EXPECTED_CONTENTS)

    contents = Path(filename).read_text()

    assert contents == EXPECTED_CONTENTS


def test_add_key(temp_env: str) -> None:
    expected_lines = EXPECTED_CONTENTS.split("\n")
    expected_lines.append("NEWVALUE=testing")

    args = ["newvalue", "testing", "--file", temp_env]

    env_cli.main(args)

    with open(temp_env) as tempfile:
        results = tempfile.read()

    assert results == "\n".join(expected_lines)


def test_main_returns_code_on_error(temp_env: str) -> None:
    args = ["TEST1", "exists", "-F", temp_env]
    result = env_cli.main(args)
    assert result


def test_add_key_raises_when_exists() -> None:
    with pytest.raises(KeyError):
        env_cli._add_key("TEST1", "some value", EXPECTED_CONTENTS)


def test_update_key(temp_env: str) -> None:
    expected = EXPECTED_CONTENTS.replace("value_one", "new_value")
    args = ["-U", "TEST1", "new_value", "--file", temp_env]

    env_cli.main(args)

    with open(temp_env) as tempfile:
        results = tempfile.read()

    assert results == expected


def test_update_key_raises_when_not_exists() -> None:
    with pytest.raises(KeyError):
        env_cli._update_key("NEWKEY", "some value", EXPECTED_CONTENTS)


def test_delete_key(temp_env: str) -> None:
    lines = [n for n in EXPECTED_CONTENTS.split("\n") if not n.startswith("export")]
    expected = "\n".join(lines)
    args = ["TEST1", "--delete", "-F", temp_env]

    env_cli.main(args)

    with open(temp_env) as tempfile:
        results = tempfile.read()

    assert results == expected


def test_delete_key_raises_when_not_exists() -> None:
    with pytest.raises(KeyError):
        env_cli._delete_key("NEWKEY", EXPECTED_CONTENTS)
