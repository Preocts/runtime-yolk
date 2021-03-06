# runtime-yolk

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/runtime-yolk/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/runtime-yolk/main)
[![Python package](https://github.com/Preocts/runtime-yolk/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/runtime-yolk/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/Preocts/runtime-yolk/branch/main/graph/badge.svg?token=sn79oOaqRI)](https://codecov.io/gh/Preocts/runtime-yolk)

## Requirements

- [Python](https://python.org) >= 3.8


Load your local `.env` file to environ, load your application.ini which can be
environment specific, and setup basic logging behavior all with a single call.
Designed to be low effort, runtime-yolk works well in the initial entry point of
a project and doesn't add additional requires to downstream libraries.

- Environment variables are loaded from the `.env` file, or specified source,
  directly to `os.environ`. This allows other processes to pull directly from
  the environ and reduces library coupling.

- Configuration files are loaded as ConfigParser objects (stdlib). The loading
  layers each consecutive file allowing flexible environment specific configs to
  be leveraged.  A custom `{{key}}` string interpolation is used when loading
  config files to allow environ vars to be injected into the config. If the
  requested key cannot be interpolated the literal value is kept instead of
  raising exceptions. `%` is also safe for all api-token/key needs.

- Set logging levels and format initially from the configuration. Helper methods
  for creating a logger for the entry script, define logging level, or add
  `FileHandlers` make setup easier.



## Road Map
As a work in progress, the road-map is loosely followed:

- [X] Hot load parameter (run all loaders)
- [X] Configuration loading
  - [X] load a application.ini in project root, assume some defaults if missing
    - [X] project default environment
    - [X] project default environ var names
      - [X] environment
      - [X] logging level
      - [X] custom
- [X] Logger init
  - [X] Create a logger or apply logging style to existing (think AWS lambda)
  - [X] setters for format, handlers, etc
  - [X] defaults loaded from default.ini (optional if exists)
- [X] Secrets loader (.env)
  - [X] auto load off by default
  - [X] discovery in cwd
  - [X] cli `yolk-env [-h] [-U] [-D] [-F FILE] key [value]`
- [ ] Spike: load json/yaml/toml ?
  - Return custom dict-like object versus ConfigParser
  - All should translate to a nested-dict structure
  - Detect by file extension or ask-forgiveness loading?
  - Alternative `.load_config(type=...)` keeping `.ini` default behavior
- [ ] Documentation for use
- [ ] Example files
- [ ] pypi deployable in CI

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

| PHONY             | Description                                                           |
| ----------------- | --------------------------------------------------------------------- |
| `init`            | Update pip to newest version                                          |
| `install`         | install the project                                                   |
| `install-test`    | install test requirements and project as editable install             |
| `install-dev`     | install development/test requirements and project as editable install |
| `build-dist`      | Build source distribution and wheel distribution                      |
| `clean-artifacts` | Deletes python/mypy artifacts, cache, and pyc files                   |
| `clean-tests`     | Deletes tox, coverage, and pytest artifacts                           |
| `clean-build`     | Deletes build artifacts                                               |
| `clean-all`       | Runs all clean scripts                                                |
