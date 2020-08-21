# python-seed

<p align="center">
  <img src="https://user-images.githubusercontent.com/10407788/90814089-905bf800-e2f6-11ea-8bd7-2639fa1177af.png" style="max-width: 800px;" alt="python-seed"></a>
</p>
<p align="center">
  <em>Starter kit for creating a new python package.</em>
</p>
<p align="center">
  <a href="https://github.com/developmentseed/python-seed/actions?query=workflow%3ACI" target="_blank">
      <img src="https://github.com/developmentseed/python-seed/workflows/CI/badge.svg" alt="Test">
  </a>
  <a href="https://codecov.io/gh/developmentseed/python-seed" target="_blank">
      <img src="https://codecov.io/gh/developmentseed/python-seed/branch/master/graph/badge.svg" alt="Coverage">
  </a>
  <a href="https://pypi.org/project/python-seed" target="_blank">
      <img src="https://img.shields.io/pypi/v/python-seed?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://github.com/developmentseed/python-seed/blob/master/LICENSE" target="_blank">
      <img src="https://img.shields.io/github/license/developmentseed/python-seed.svg" alt="Downloads">
  </a>
</p>

This is a starter repo for creating a new python package. Included are templates for standard files as well as best practices.

## Install

You can install python-seed using pip

```bash
$ pip install -U pip
$ pip install python-seed
```

or install from source:

```bash
$ git clone https://github.com/developmentseed/python-seed.git
$ cd python-seed
$ pip install -U pip
$ pip install -e .
```

## Usage

```bash
$ pyseed --help
Usage: pyseed [OPTIONS] COMMAND [ARGS]...

  python-seed subcommands.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  create  Create new python seed skeleton
```

```
$ pyseed create --help
Usage: pyseed create [OPTIONS] NAME

  Create new python seed skeleton.

Options:
  --ci [circleci|github]  Add CI configuration
  --help                  Show this message and exit.
```

Create a new python project

```bash
# Create a project without CI
$ pyseed create awesomepythonproject

# List files created
$ ls -1 awesomepythonproject
.pre-commit-config.yaml
README.md
awesomepythonproject/
requirements-dev.txt
requirements.txt
setup.py
tests/
tox.ini
```

With CI framework

```bash
# Create a project github actions
$ pyseed create awesomepythonproject --ci github

# List files created
$ ls -1 awesomepythonproject
.github/workflows/ci.yml
codecov.yml
.pre-commit-config.yaml
README.md
awesomepythonproject/
requirements-dev.txt
requirements.txt
setup.py
tests/
tox.ini
```

# Project structure

```
my-project/
 ├── .circleci/ or .github/      - CI configuration.
 ├── codecov.yml                 - codecov configuration (only if CI is added).
 ├── .pre-commit-config.yaml     - pre-commit configuration.
 ├── README.md                   - project readme.
 ├── my_project/                 - core python module.
 ├── tests/                      - tests suite placeholder for your module.
 ├── requirements.txt            - python requirements (!!! by default requirements are written in setup.py)
 ├── requirements-dev.txt        - python dev requirements (!!! by default requirements are written in setup.py)
 └──tox.ini                      - TOX configuration.
```


## Contribution & Development

Issues and pull requests are more than welcome.

**dev install**

```bash
$ git clone https://github.com/developmentseed/python-seed.git
$ cd python-seed
$ pip install -e .[dev]
```

**Python3.7 only**

This repo is set to use `pre-commit` to run *isort*, *flake8*, *pydocstring*, *black* ("uncompromising Python code formatter") and mypy when committing new code.

```bash
$ pre-commit install
```

## About
python-seed was created by [Development Seed](<http://developmentseed.org>)
