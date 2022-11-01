[![Python 3.7 | 3.8 | 3.9 | 3.10 | 3.11](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/downloads)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/runtime-yolk/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/runtime-yolk/main)
[![Python tests](https://github.com/Preocts/runtime-yolk/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/runtime-yolk/actions/workflows/python-tests.yml)

# runtime-yolk

## Requirements

- [Python](https://python.org) >= 3.7

Load your local `.env` file to environ, load your application.ini which can be
environment specific, and setup basic logging behavior all with a single call.
Designed to be low effort, runtime-yolk works well in the initial entry point of
a project and doesn't add additional requires to downstream libraries.

- Environment variables are loaded from the `.env` file, or specified source,
  directly to `os.environ`. This allows other processes to pull directly from
  the environ and reduces library coupling.

- Configuration files are loaded as `ConfigParser` objects. The loading
  layers each consecutive file allowing flexible environment specific configs to
  be leveraged.  A custom `{{key}}` string interpolation is used when loading
  config files to allow environ vars to be injected into the config. If the
  requested key cannot be interpolated the literal value is kept instead of
  raising exceptions. `%` is also safe for all api-token/key needs.

- Set logging levels and format initially from the configuration. Helper methods
  for creating a logger for the entry script, define logging level, or add
  `FileHandlers` make setup easier.

---

## Installation

From github:

```shell
$ python -m pip install git+https://github.com/Preocts/runtime-yolk@#.#.#
```

Replace the `#.#.#` with the desired version or `@main` for the latest (unstable).

From pypi:

```shell
$ python -m pip install runtime-yolk
```

---

## Usage Examples

#### [Loading runtime setup manually](examples/manual_loading.py)

#### [Loading runtime setup automatically](examples/auto_loading.py)

### Setup of `application.ini`

The default configuration file looked for loading is `application.ini`. This can be change on call of `.load_config()` if desired. There are no required fields in the configuration file. However, a few will impact `runtime-yolk`'s behavior directly when present in the `[DEFAULT]` section:

- `logging_level` : When set, `.set_logging()` will use this logging level
- `logging_format` : Allow overriding the default logging format template used.
  - Default is `%(asctime)s - %(levelname)s - %(name)s - %(message)s`
- `environment` : When defined the value will be used to load additional `application-[environment].ini` configuration files. These can be chained however will break the loading loop on a file that has already been loaded.

Sample:

```ini
[DEFAULT]
logging_level = DEBUG
logging_format = %(asctime)s - %(levelname)s - %(name)s - %(message)s
environment = {{ENVIRONMENT}}
```

### `.env` file loading

`.env` files are loaded with the expectation of key = value pairs. `#` comments are allowed as well as blank lines.

Current format for the `.env` file supports strings only and is parsed in
the following order:

1. Each separate line is considered a new possible key/value set
2. Each set is delimited by the first `=` found
3. Leading and trailing whitespace are removed
4. Removes leading 'export ' prefix, case agnostic
5. Matched leading/trailing single quotes or double quotes will be
  stripped from values (not keys).

Sample:

```ini
# OAuth token goes here, do not commit this Glenn
SAMPLE_TOKEN=somesecrettokenforuse
ENVIRONMENT=sandbox
```

---

---

# Local developer installation

It is **strongly** recommended to use a virtual environment
([`venv`](https://docs.python.org/3/library/venv.html)) when working with python
projects. Leveraging a `venv` will ensure the installed dependency files will
not impact other python projects or any system dependencies.

The following steps outline how to install this repo for local development. See
the [CONTRIBUTING.md](CONTRIBUTING.md) file in the repo root for information on
contributing to the repo.

**Windows users**: Depending on your python install you will use `py` in place
of `python` to create the `venv`.

**Linux/Mac users**: Replace `python`, if needed, with the appropriate call to
the desired version while creating the `venv`. (e.g. `python3` or `python3.8`)

**All users**: Once inside an active `venv` all systems should allow the use of
`python` for command line instructions. This will ensure you are using the
`venv`'s python and not the system level python.

---

## Installation steps

Clone this repo and enter root directory of repo:

```console
$ git clone https://github.com/Preocts/runtime-yolk
$ cd runtime-yolk
```

Create the `venv`:

```console
$ python -m venv venv
```

Activate the `venv`:

```console
# Linux/Mac
$ . venv/bin/activate

# Windows
$ venv\Scripts\activate
```

The command prompt should now have a `(venv)` prefix on it. `python` will now
call the version of the interpreter used to create the `venv`

Install editable library and development requirements:

```console
# Update pip and tools
$ python -m pip install --upgrade pip

# Install editable version of library
$ python -m pip install --editable .[dev]
```

Install pre-commit [(see below for details)](#pre-commit):

```console
$ pre-commit install
```

---

## Misc Steps

Run pre-commit on all files:

```console
$ pre-commit run --all-files
```

Run tests:

```console
$ tox [-r] [-e py3x]
```

Build dist:

```console
$ python -m pip install --upgrade build

$ python -m build
```

To deactivate (exit) the `venv`:

```console
$ deactivate
```
---

## Note on flake8:

`flake8` is included in the `requirements-dev.txt` of the project. However it
disagrees with `black`, the formatter of choice, on max-line-length and two
general linting errors. `.pre-commit-config.yaml` is already configured to
ignore these. `flake8` doesn't support `pyproject.toml` so be sure to add the
following to the editor of choice as needed.

```ini
--ignore=W503,E203
--max-line-length=88
```

---

## [pre-commit](https://pre-commit.com)

> A framework for managing and maintaining multi-language pre-commit hooks.

This repo is setup with a `.pre-commit-config.yaml` with the expectation that
any code submitted for review already passes all selected pre-commit checks.
`pre-commit` is installed with the development requirements and runs seemlessly
with `git` hooks.

---

## Makefile

This repo has a Makefile with some quality of life scripts if the system
supports `make`.  Please note there are no checks for an active `venv` in the
Makefile.

| PHONY         | Description                                                                |
| ------------- | -------------------------------------------------------------------------- |
| `init`        | Update pip to newest version                                               |
| `install`     | install the project                                                        |
| `install-dev` | install development/test requirements and project as editable install      |
| `upgrade-dev` | update all dependencies, regenerate requirements.txt (disabled by default) |
| `coverage`    | Runs `tox -p`. results to stdout, json, and html                           |
| `build-dist`  | Build source distribution and wheel distribution                           |
| `clean`       | Deletes build, tox, coverage, pytest, mypy, cache, and pyc artifacts       |
