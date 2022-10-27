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
            self.set_logging()

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

    def set_logging(self, level: str | int | None = None) -> None:
        """
        Set the root log level for stderr output. If empty, config level is used.

        Args:
            level: String or Int representing logging level. (e.g.: "ERROR" or 40)
        """
        config_level = self.config.get("DEFAULT", "logging_level", fallback="ERROR")
        config_fmt = self.config.get("DEFAULT", "logging_format", fallback="")

        # Create our handler for root logger, don't touch existing handlers
        handler = logging.StreamHandler()
        handler.set_name("yolk_core")
        handler.setFormatter(logging.Formatter(config_fmt))
        logging.getLogger().addHandler(handler)

        # Apply desired level to root logger
        logging.getLogger().setLevel(level if level is not None else config_level)

    def get_logger(self, name: str | None = None) -> logging.Logger:
        """Return a logger. If a name is not provided, root logger is returned."""
        return logging.getLogger(name)

    def add_logging_file(
        self,
        filepath: str,
        level: str | int | None = None,
        append: bool = True,
    ) -> None:
        """
        Add a handler for logging output to desired file.

        Args:
            filepath: Path and filename to write logs. Relative or Absolute.
            level: String or Int representing logging level. (e.g.: "DEBUG" or 10)
            append: If False, existing log file will be cleared before writing
        """
        # Assert we have a level, default to lowest.
        config_level = self.config.get("DEFAULT", "logging_level", fallback="DEBUG")
        level = level if level is not None else config_level

        handler = logging.FileHandler(filename=filepath, mode="a" if append else "w")
        handler.set_name(f"yolk_core_{filepath}")
        handler.setLevel(level)

        logging.getLogger().addHandler(handler)
