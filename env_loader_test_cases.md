# env_loader.py Draft

## Rules applied to parsing `.env` file

Current format for the `.env` file supports strings only and is parsed in
the following order:

1. Each separate line is considered a new possible key/value set
1. Each set is delimited by the first `=` found
1. Leading and trailing whitespace are removed
1. Removes leading 'export ' prefix, case agnostic
1. Matched leading/trailing single quotes or double quotes will be
  stripped from values (not keys).


## No .env file present

Setup:

- No `.env` file exists

Expectations:

- Loader will quietly pass without taking action

```py
from runtime_yolk import Yolk

runtime = Yolk()
```

## Load .env located in project root

Setup:

- `.env` exists in `./` of project


Expectations:

- Run-time environment will have valid values from `.env`

```py
from runtime_yolk import Yolk

runtime = Yolk()
```

`.env`

```ini
    "SECRETBOX_TEST_PROJECT_ENVIRONMENT=sandbox",
    "#What type of .env supports comments?",
    "",
    "BROKEN KEY",
    "VALID==",
    "SUPER_SECRET  =          12345",
    "PASSWORD = correct horse battery staple",
    'USER_NAME="not_admin"',
    "MESSAGE = '    Totally not an \"admin\" account logging in'",
    "  SINGLE_QUOTES = 'test'",
    "export NESTED_QUOTES = \"'Double your quotes, double your fun'\"",
    '   eXport SHELL_COMPATIBLE = "well, that happened"',
```

Expected `os.environ` to contain:

```py
{
    "SECRETBOX_TEST_PROJECT_ENVIRONMENT": "sandbox",
    "VALID": "=",
    "SUPER_SECRET": "12345",
    "PASSWORD": "correct horse battery staple",
    "USER_NAME": "not_admin",
    "MESSAGE": '    Totally not an "admin" account logging in',
    "SINGLE_QUOTES": "test",
    "NESTED_QUOTES": "'Double your quotes, double your fun'",
    "SHELL_COMPATIBLE": "well, that happened",
}
```
