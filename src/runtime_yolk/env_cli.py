from __future__ import annotations

import re
from argparse import ArgumentParser
from argparse import Namespace


def _parse_args(arg_list: list[str] | None = None) -> Namespace:
    """Parse sys.argv."""
    parser = ArgumentParser("Add, update, or remove env values from .env file.")
    parser.add_argument(
        "key",
        type=str,
        help="Name of environ variable to save.",
    )
    parser.add_argument(
        "value",
        type=str,
        default="",
        nargs="?",
        help="Value to save.",
    )
    parser.add_argument(
        "-U",
        "--update",
        action="store_true",
        help="Update existing value.",
    )
    parser.add_argument(
        "-D",
        "--delete",
        action="store_true",
        help="Delete existing key.",
    )
    parser.add_argument(
        "-F",
        "--file",
        action="store",
        default=".env",
        help="Specify filename and path, default is '.env'",
    )
    return parser.parse_args(arg_list)


def _read_file(file_: str) -> str:
    """Read in given file if exists, otherwise return empty string."""
    try:
        with open(file_) as infile:
            return infile.read()
    except FileNotFoundError:
        return ""


def _write_file(file_: str, contents: str) -> None:
    """Write contents to file as provided."""
    with open(file_, "w") as outfile:
        outfile.write(contents)


def _add_key(key: str, value: str, contents: str) -> str:
    """Add key=value to contents, returns contents. Raises KeyError if key exists."""
    if re.search(rf"{key.upper()}(\s+)?=", contents):
        raise KeyError("Key already exists in target file.")

    lines = contents.split("\n")
    lines.append(f"{key.upper()}={value}")
    return "\n".join(lines)


def _update_key(key: str, value: str, contents: str) -> str:
    """Update key=value, returns contents. Raises KeyError if key is missing."""
    sub_pattern = re.compile(rf"{key.upper()}(\s+)?=.+")

    if not sub_pattern.search(contents):
        raise KeyError("Key to update was not found in file.")

    return sub_pattern.sub(f"{key.upper()}={value}", contents)


def _delete_key(key: str, contents: str) -> str:
    """Delete key, returns contents. Raises KeyError if key is missing."""
    sub_pattern = re.compile(rf"{key.upper()}(\s+)?=.+")

    if not sub_pattern.search(contents):
        raise KeyError("Key to update was not found in file.")
    lines = [line for line in contents.split("\n") if not sub_pattern.search(line)]

    return "\n".join(lines)


def main(_args: list[str] | None = None) -> int:
    """Entry point for cli."""
    args = _parse_args(_args)

    contents = _read_file(args.file)
    try:
        if args.delete:
            contents = _delete_key(args.key, contents)
        elif args.update:
            contents = _update_key(args.key, args.value, contents)
        else:
            contents = _add_key(args.key, args.value, contents)
    except KeyError as error:
        print(f"Error: {error}")
        return 1

    _write_file(args.file, contents)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
