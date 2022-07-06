"""Load and store configuration data"""
from __future__ import annotations

import os
from configparser import ConfigParser
from pathlib import Path

from runtime_yolk.util.file_rule import get_file_name

DEFAULT_DEFAULT = {
    "environment": "",
    "logging_level": "DEBUG",
}
DEFAULT_ENVIROMENT_VARIABLES = {
    "environment": "YOLK_ENVIRONMENT",
    "logging_level": "YOLK_LOGGING_LEVEL",
}
CWD = Path().cwd()


class Config:
    """Load and store configuration data"""

    yolk_environment_key = "YOLK_ENVIRONMENT"

    def __init__(self) -> None:
        """Create a new instance of Config."""
        # Build and prime the default config. Values will be replaced by any
        # loaded configurations.
        self._config = ConfigParser()
        self._config["DEFAULT"] = DEFAULT_DEFAULT
        self._config["ENVIRONMENT_VARIABLES"] = DEFAULT_ENVIROMENT_VARIABLES

        self._environment = self._fetch_environment()
        # Store loaded config file names to prevent loading the same file twice.
        self._loaded_configs: set[str] = set()

    def load(
        self,
        *,
        config_name: str = "yolk_application",
        load_additional: bool = True,
    ) -> None:
        """
        Load configuration data from a file.

        Looks for the `config_file` in the working directory. After loading
        the config_file, if `load_additional`, the environment value is appended
        to the filename before the file extension. e.g. `yolk_application.ini` becomes
        `yolk_application_${yolk_environment}.ini`. If found, this config
        is loaded next and the process repeats.

        Args:
            config_name: The name of the configuration file without the extension.
            load_additional: When true, environment labeled configurations are loaded.
        """
        self._load(config_name, "", load_additional)

    def _fetch_environment(self) -> str:
        """Get environment value from config, environ, or return empty string."""
        config_env = self._config.get("DEFAULT", "environment", fallback="")
        return config_env or os.getenv(self.yolk_environment_key) or ""

    def _update_environment_key(self) -> None:
        """Update the key for environment variable values from loaded config."""
        self.yolk_environment_key = self._config.get(
            section="ENVIRONMENT_VARIABLES",
            option="yolk_environment",
            fallback=self.yolk_environment_key,
        )

    def _load(
        self,
        config_file: str,
        yolk_environment: str,
        load_additional: bool,
    ) -> None:
        """Interal recursive loader."""
        _file = CWD / Path(get_file_name(config_file, yolk_environment))

        if _file.is_file() and str(_file) not in self._loaded_configs:
            self._config.read(_file)

            self._loaded_configs.add(str(_file))
            self._update_environment_key()
            self._environment = self._fetch_environment()

            # If the config file has an environment set, load the environment file.
            if load_additional and self._environment:
                self._load(config_file, self._environment, load_additional)

    # def save(self, config_file: str = "yolk_application.ini") -> None:
    #     """Save configuration data to a file."""
    #     with open(config_file, "w") as _file:
    #         self._config.write(_file)

    def get_config(self) -> ConfigParser:
        """Get the config object."""
        return self._config

    # def set_config(self, config: ConfigParser) -> None:
    #     """Set the config object."""
    #     self._config = config
