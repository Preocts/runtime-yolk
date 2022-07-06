"""
Load local .env file into environment variables.

Current format for the `.env` file supports strings only and is parsed in
the following order:
- Each seperate line is considered a new possible key/value set
- Each set is delimted by the first `=` found
- Leading and trailing whitespace are removed
- Removes leading 'export ' prefix, case agnostic
- Matched leading/trailing single quotes or double quotes will be
  stripped from values (not keys).
"""
from __future__ import annotations

import os
import re
from pathlib import Path

CWD = Path().cwd()


class EnvLoader:
    """Load local .env file into environment variables."""

    LT_DBL_QUOTES = r'^".*"$'
    LT_SGL_QUOTES = r"^'.*'$"
    EXPORT_PREFIX = r"^\s*?export\s"

    def run(self, filename: str | None = None) -> bool:
        """
        Load file to environ.

        Args:
            filename: Name of environment file to load (default: ".env")
        """
        filename = str(CWD / Path(filename)) if filename else str(CWD / Path(".env"))

        loaded_values = self._load_values(filename)

        for key, value in loaded_values.items():
            os.environ[key] = value

        return bool(loaded_values)

    def _load_values(self, filename: str) -> dict[str, str]:
        """Internal: Load values from provided filename."""
        try:
            with open(filename, encoding="utf-8") as input_file:
                return self._parse_env_file(input_file.read())
        except FileNotFoundError:
            return {}

    def _parse_env_file(self, input_file: str) -> dict[str, str]:
        """Internal: Parse env file into key-pair values."""
        loaded_values: dict[str, str] = {}

        for line in input_file.split("\n"):
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
