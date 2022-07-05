from __future__ import annotations

import re


def _replace_spaces(string: str) -> str:
    """Replace spaces with underscores, removes extra spaces."""
    return re.sub(r"\s+", "_", string.strip())


def get_file_name(filename: str, environment: str) -> str:
    """Get the file name for the given filename and environment."""
    # Replace spaces with underscores, removes extra spaces, and lowercase
    filename = _replace_spaces(filename.lower())
    environment = _replace_spaces(environment.lower())

    if environment:
        parts = filename.split(".")
        if len(parts) > 1:
            prefix = ".".join(parts[0 : len(parts) - 1])
            filename = f"{prefix}_{environment}.{parts[-1]}"
        else:
            filename = f"{parts[0]}_{environment}"

    return filename
