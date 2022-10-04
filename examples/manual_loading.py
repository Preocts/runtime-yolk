from __future__ import annotations

from runtime_yolk import Yolk

runtime = Yolk()

# Load our `.env` file to the run-time environment
runtime.load_env()

# Loads, by default, the `application.ini`.
# Fields such {{ENVIRONMENT}} are populated from environment values
# Because `ENVIRONMENT=prod` exists in the environ, `application-prod`
# will also be loaded on top of `application.ini`
runtime.load_config()

# Sets the logging to the configuration level, in this case "ERROR" level
# This will not impact existing loggers
runtime.set_logging()

# Mirrors `logging.getLogger()` for convenienve
logger = runtime.get_logger(__name__)


def mock_oauth_login(token: str) -> None:
    """Imagine if you will a world of information."""


# Log in with the token from our .env which has been translated into the config
mock_oauth_login(runtime.config.get("SAMPLE_TOKEN"))
