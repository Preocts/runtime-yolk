# config_loader.py Draft

## Load with no default config

Setup:

- No `application.ini` exists

Expectations:

- A default config is created in memory
  - `logging_level` is default (debug)
  - `environment` is default (empty)

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
- environment is interpolated to prod

Expectations:

- Yolk will load the default `application.ini` config
- Yolk will load the prod `application_prod.ini` config
- `logging_level` is "ERROR"
- `environment` is "prod"
- config is loaded on instantiation

`application.ini`

```ini
[DEFAULT]
logging_level = DEBUG
environment = {{ENVIRONMENT}}
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
