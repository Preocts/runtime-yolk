from __future__ import annotations

from runtime_yolk import Yolk

# Auto run the following:
#  - load our `.env` file to the run-time environment
#  - load the `application.ini` config file
#  - load the `application-prod.ini` config file
#    - This is done because ENVIRONMENT=prod in the .env
#  - set logging to the config level of "ERROR"
runtime = Yolk(auto_load=True)

# Mirrors `logging.getLogger()` for convenienve
logger = runtime.get_logger(__name__)


def mock_oauth_login(token: str) -> None:
    """Imagine if you will a world of information."""


# Log in with the token from our .env which has been translated into the config
mock_oauth_login(runtime.config.get("SAMPLE_TOKEN"))
