from __future__ import annotations

from runtime_yolk import env_cli


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
