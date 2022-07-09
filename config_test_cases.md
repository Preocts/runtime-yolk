# config_loader.py Draft

## Load with no default config

Setup:

- No `application.ini` exists

Expectations:

- A default config is created in memory
  - `logging_level` is default
  - `environment` is default
- Default environmental variable keys are used
  - `YOLK_ENVIRONMENT` is used to label environment and load additional configs
  - `YOLK_LOGGING_LEVEL` is used to set logging level

`example.py`

```py
from runtime_yolk import Yolk

runtime = Yolk()
runtime.load_config()
```

## Load with default config and env config

Setup:

- `application.ini` exists
- `application_prod.ini` exits
- `ENVIRONMENT=prod` set in environment vars
- Change environment variable housing environment name to `ENVIRONMENT`

Expectations:

- Yolk will load the default `application.ini` config
- Yolk will load the prod `application_prod.ini` config
- `logging_level` is "ERROR"
- `environment` is "prod"

`application.ini`

```ini
[DEFAULT]
logging_level = DEBUG
environment =

[ENVIRONMENT_VARIABLES]
yolk_environment = ENVIRONMENT
yolk_logging_level = YOLK_LOGGING_LEVEL
```

`application_prod.ini`

```ini
[DEFAULT]
logging_level = ERROR
environment = prod
```

`example.py`

```py
from runtime_yolk import Yolk

runtime = Yolk(auto_load=True)
```
