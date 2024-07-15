# Python dependency version checker

![Icon](./docs/icon.png?raw=true "Icon")

## Why use this tool?

If you are using Poetry for python dependency management it can help you to decide if you need to update a dependency or not.

e.g. your `pyproject.toml` file may have a version range specified, but it may not be clear if the version in the lock file is the latest allowed by your range in the pyproject.toml file

You could run poetry show [dependency] to get the installed version, then pop over to PyPi to check the latest version but if you have a lot of dependencies, this can be time-consuming, so let this tool do it for you.

## Installation

Clone this repository and run the following commands in the root of the project:

## Usage

```bash
poetry install
poetry run check [-r] [local or remote]
```

Steps:

- Enter the url for your remote repository or the path to your local repository
- Choose the branch to checkout and run the report on
- If multiple Dockerfiles are found, choose the one to inspect

## Options

- `-r` - Output a printable report to a file (report.html)
- `local` - Check a local repository (a folder relative to the directory this script is run from)
- `remote` - Check a remote repository

Command help is available:

```bash
poetry run check --help
poetry run check remote --help
poetry run check local --help
```

## Limitations

- Only works if the Dockerfile uses poetry to install dependencies

## TODO

- Add support for different dependency managers (requirements.txt, etc.)

## How it works

It will do the following:

- clone the repository and checkout the specified branch for a remote repository
- analyse the local folder if running against a local repository
- find & inspect the Dockerfile to find the docker image version and poetry version used
- build a new image based on the Dockerfile image and export the dependency list using poetry export -> requirements-frozen.txt
- compare each dependency version in requirements-frozen.txt with the latest version on PyPi if it is listed in the pyproject.toml file
- output the results in the console and indicate if there are any outdated dependencies and/or manual checks required
- optionally output a report to a file

e.g. Console output

![Console ouput](./docs/console.jpg?raw=true "Console output")
