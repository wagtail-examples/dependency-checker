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
poetry run start
```

Steps:

- Enter the url for your repository
- Choose the branch to checkout and run the report on
- If multiple Dockerfiles are found, choose the one to inspect

## Options

Options can be passed in as command line arguments or enter them when prompted.

```bash
poetry run start --help
```

- `--repo-url` - The URL of the repository to clone/check
- `--report` - Output a printable report to a file (report.html)

## Limitations

- Only works if the Dockerfile uses poetry to install dependencies

## TODO

- Add support for different dependency managers (requirements.txt, etc.)

## How it works

It will do the following:

- clone the repository and checkout the specified branch
- inspect the Dockerfile to find the image version and poetry version used
- build a new image based on the Dockerfile image and export the dependency list using poetry export -> requirements-frozen.txt
- compare each dependency version in requirements-frozen.txt with the latest version on PyPi if it is listed in the pyproject.toml file
- output the results in the console and indicate if there are any outdated dependencies and/or manual checks required

e.g. Console output

![Console ouput](./docs/console.jpg?raw=true "Console output")
