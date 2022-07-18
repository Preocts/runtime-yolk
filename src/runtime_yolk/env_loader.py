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

    LTQUOTES_RE = re.compile(r"([\"'])(.*)\1$|^(.*)$")
    EXPORT_PREFIX_RE = re.compile(r"^\s*?export\s*", flags=re.IGNORECASE)

    def __init__(self, working_directory: Path | None = None) -> None:
        """
        Create .env loader.

        Args:
            working_directory: Set the working directory where file(s) will be loaded.
        """
        self._working_directory = working_directory or Path().cwd()

    def load(self, filename: str | None = None) -> bool:
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
        """Parse env file into key-pair values."""
        loaded_values: dict[str, str] = {}

        for line in contents.split("\n"):
            if not line or line.strip().startswith("#") or len(line.split("=", 1)) != 2:
                continue
            key, value = line.split("=", 1)

            key = self._strip_export(key).strip()
            value = value.strip()
            value = self._remove_lt_quotes(value)

            loaded_values[key] = value

        return loaded_values

    def _remove_lt_quotes(self, in_: str) -> str:
        """Remove matched leading and trailing single or double quotes."""
        match = self.LTQUOTES_RE.match(in_)
        return match.group(2) if match and match.group(2) else in_

    def _strip_export(self, in_: str) -> str:
        """Remove leading 'export ' prefix, case agnostic."""
        return self.EXPORT_PREFIX_RE.sub("", in_)
