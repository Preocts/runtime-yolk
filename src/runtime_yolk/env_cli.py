from __future__ import annotations

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


def _save_file(file_: str, contents: str) -> None:
    """Save contents to file as provided."""
    with open(file_, "w") as outfile:
        outfile.write(contents)


def main() -> int:
    """Entry point for cli."""
    # pragma: no cover
    args = _parse_args()
    print(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
