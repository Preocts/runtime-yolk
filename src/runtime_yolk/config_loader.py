"""Load and store configuration data"""
from __future__ import annotations

import os
import re
from configparser import ConfigParser
from pathlib import Path

from runtime_yolk.util.file_rule import get_file_name

INTERPOLATE_PATTERN = "{{(.+?)}}"


class ConfigLoader:
    """Load and store configuration data"""

    def __init__(self, *, working_directory: Path | None = None) -> None:
        """
        Create a new instance of Config.

        Args:
            working_directory: Set the working directory where file(s) will be loaded.
        """
        self._working_directory = working_directory or Path().cwd()
        self._config = ConfigParser(interpolation=None)

        self._build_default_config()

        # Store loaded config file names to prevent loading the same file twice.
        self._loaded_configs: set[Path] = set()

    def _build_default_config(self) -> None:
        """Build and populate the default config."""
        self._config["DEFAULT"] = {
            "environment": os.getenv("ENVIRONMENT", ""),
            "logging_level": os.getenv("LOGGING_LEVEL", "ERROR"),
            "logging_format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        }

    def load(
        self,
        *,
        config_name: str = "application",
    ) -> None:
        """
        Load configuration data from a file, layers loads onto existing loaded data.

        Looks for the `${config_name}.ini` in the working directory. After loading the
        config_name the environment value is appended to the filename before the file
        extension. e.g. `application.ini` becomes `application_${environment}.ini`. If
        found, this config is loaded next.

        Default ConfigParser interpolation is disabled. Values with the pattern of
        `{{KEYWORD}}` are interpolated a single time against matching environ keys.
        Keywords are case sensitive.

        Args:
            config_name: The name of the configuration file without the extension.
        """
        self._load(config_name, "")

    def _load(self, config_file: str, yolk_environment: str) -> None:
        """Interal recursive loader."""

        _file = self._working_directory / get_file_name(config_file, yolk_environment)

        if _file.is_file() and _file not in self._loaded_configs:
            contents = self._interpolate_environment(_file.read_text())

            # Load the discovered content as a configuration string
            # ConfigParser handles invalid content
            self._config.read_string(contents)
            self._loaded_configs.add(_file)

            # If the config file has an environment set, attempt to load the next file.
            if self._config.get("DEFAULT", "environment", fallback=None):
                self._load(config_file, self._config.get("DEFAULT", "environment"))

    def _interpolate_environment(self, contents: str) -> str:
        """Interpolate {{keywords}} to matching environment variable values."""
        for match in re.finditer(INTERPOLATE_PATTERN, contents):
            contents = re.sub(match.group(0), os.getenv(match.group(1), ""), contents)
        return contents

    def get_config(self) -> ConfigParser:
        """Get the config object."""
        return self._config
