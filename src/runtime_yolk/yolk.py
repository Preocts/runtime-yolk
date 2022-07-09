"""
Main class for runtime-yolk.

Reponsible for all loaders and runners.
"""
from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

from runtime_yolk.config_loader import ConfigLoader
from runtime_yolk.env_loader import EnvLoader


class Yolk:
    """Create a single class for run-time initiation tasks."""

    def __init__(
        self,
        *,
        working_directory: str | None = None,
    ) -> None:
        """Super powerful docstring."""
        if working_directory:
            self._working_directory = Path(working_directory)
        else:
            self._working_directory = Path.cwd()

        self._config = ConfigLoader(working_directory=self._working_directory)
        self._env = EnvLoader(working_directory=self._working_directory)

    @property
    def config(self) -> ConfigParser:
        """Return loaded ConfigParser object."""
        return self._config.get_config()
