from __future__ import annotations

import re


def _replace_spaces(string: str) -> str:
    """Replace spaces with underscores, removes extra spaces."""
    return re.sub(r"\s+", "_", string.strip())


def get_file_name(filename: str, environment: str = "") -> str:
    """Get the file name for the given filename, adding environment if provided."""
    # Replace spaces with underscores, removes extra spaces, and lowercase
    filename = _replace_spaces(filename.lower())

    if environment:
        environment = _replace_spaces(environment.lower())
        filename = f"{filename}-{environment}"

    return f"{filename}.ini"
