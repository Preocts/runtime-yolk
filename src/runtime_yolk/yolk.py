"""
Main class for runtime-yolk.

Reponsible for all loaders and runners.
"""
from __future__ import annotations

import logging
from configparser import ConfigParser
from pathlib import Path

from runtime_yolk.config_loader import ConfigLoader
from runtime_yolk.env_loader import EnvLoader


class Yolk:
    """Create a single class for run-time initiation tasks."""

    def __init__(
        self,
        *,
        auto_load: bool = False,
        working_directory: str | None = None,
    ) -> None:
        """
        Create Yolk run-time loader instance.

        Keyword Args:
            auto_load: Run loads on instantiation. (default: False)
            working_directory: Defaults to cwd, provide path to where config files
        """
        if working_directory:
            self._working_directory = Path(working_directory)
        else:
            self._working_directory = Path.cwd()

        self._config = ConfigLoader(working_directory=self._working_directory)
        self._env = EnvLoader(working_directory=self._working_directory)

        if auto_load:
            self.load_env()
            self.load_config()

    @property
    def config(self) -> ConfigParser:
        """Return loaded ConfigParser object."""
        return self._config.get_config()

    def load_config(self, config_name: str = "application") -> None:
        """
        Load configuration from a file, layers loads onto existing loaded data.

        Args:
            config_name: The name of the config file without the extension
        """
        self._config.load(config_name=config_name)

    def load_env(self, filename: str = ".env") -> None:
        """
        Load environment values from a file.

        Args:
            filename: The name of the env file to load. (default: `.env`)
        """
        self._env.load(filename)

    def add_logging(self, level: str | int | None = None) -> None:
        """
        Set the root log level for stderr output. If empty, config level is used.

        Args:
            level: String or Int representing logging level. (e.g.: "DEBUG", 10)
        """
        level = level.upper() if isinstance(level, str) else level
        config_level = self.config.get("DEFAULT", "logging_level", fallback="DEBUG")
        config_fmt = self.config.get("DEFAULT", "logging_format", fallback="")

        # Create our handler for logs, don't touch existing handlers
        handler = logging.StreamHandler()
        handler.set_name("yolk_core")
        handler.setFormatter(logging.Formatter(config_fmt))
        # handler.setLevel(level if level is not None else config_default)
        logging.getLogger().setLevel(level if level is not None else config_level)
        logging.getLogger().addHandler(handler)
