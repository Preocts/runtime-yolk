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


def main() -> int:
    """Entry point for cli."""
    # pragma: no cover
    args = _parse_args()
    print(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
