"""
Load local .env file into environment variables.

Current format for the `.env` file supports strings only and is parsed in
the following order:
- Each separate line is considered a new possible key/value set
- Each set is delimited by the first `=` found
- Leading and trailing whitespace are removed
- Removes leading 'export ' prefix, case agnostic
- Matched leading/trailing single quotes or double quotes will be
  stripped from values (not keys).
"""
from __future__ import annotations

import os
import re
from pathlib import Path


class EnvLoader:
    """Load local .env file into environment variables."""

    LT_DBL_QUOTES = r'^".*"$'
    LT_SGL_QUOTES = r"^'.*'$"
    EXPORT_PREFIX = r"^\s*?export\s*"

    def __init__(self, working_directory: Path | None = None) -> None:
        """
        Create .env loader.

        Args:
            working_directory: Set the working directory where file(s) will be loaded.
        """
        self._working_directory = working_directory or Path().cwd()

    def run(self, filename: str | None = None) -> bool:
        """
        Load file to environ.

        Args:
            filename: Name of environment file to load (default: ".env")
        """
        filename = ".env" if not filename else filename
        filepath = self._working_directory / filename

        loaded_values = self._load_values(filepath)

        for key, value in loaded_values.items():
            os.environ[key] = value

        return bool(loaded_values)

    def _load_values(self, filepath: Path) -> dict[str, str]:
        """Internal: Load values from provided filename."""
        try:
            return self._parse_env_file(filepath.read_text())

        except FileNotFoundError:
            return {}

    def _parse_env_file(self, contents: str) -> dict[str, str]:
        """Internal: Parse env file into key-pair values."""
        loaded_values: dict[str, str] = {}

        for line in contents.split("\n"):
            if not line or line.strip().startswith("#") or len(line.split("=", 1)) != 2:
                continue
            key, value = line.split("=", 1)

            key = self.strip_export(key).strip()
            value = value.strip()

            if value.startswith('"'):
                value = self.remove_lt_dbl_quotes(value)
            elif value.startswith("'"):
                value = self.remove_lt_sgl_quotes(value)

            loaded_values[key] = value

        return loaded_values

    def remove_lt_dbl_quotes(self, in_: str) -> str:
        """Remove matched leading and trailing double quotes."""
        return in_.strip('"') if re.match(self.LT_DBL_QUOTES, in_) else in_

    def remove_lt_sgl_quotes(self, in_: str) -> str:
        """Remove matched leading and trailing double quotes."""
        return in_.strip("'") if re.match(self.LT_SGL_QUOTES, in_) else in_

    def strip_export(self, in_: str) -> str:
        """Remove leading 'export ' prefix, case agnostic."""
        return re.sub(self.EXPORT_PREFIX, "", in_, flags=re.IGNORECASE)
