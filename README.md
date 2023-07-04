# Dependency version checker for Python

## Installation

Clone this repository and run the following commands in the root of the project:

## Usage

```bash
poetry install
poetry run start
```

Enter the url for your repository and the branch you want to check.

## Options

```bash
poetry run start --help
```

## Limitations

- Only works if the site is run using a Dockerfile in the root of the repository
- Only works if the Dockerfile is named `Dockerfile`
- Only works if the Dockerfile uses poetry to install dependencies

## TODO

- Add support for Dockerfile in subdirectory
- Add support for Dockerfile with different name
- Add support for different dependency managers (requirements.txt, etc.)

## How it works

- It will clone the repository and checkout the specified branch
- It will then inspect the Dockerfile to find the image version and poetry version used
- It will then build a new image and export the dependency list using poetry export -> requirements-frozen.txt
- It will then compare each dependency version in the requirements-frozen.txt with the latest version on PyPi
- It will then output the results in the console and indicate if there are any outdated dependencies

e.g. Console output

![Console ouput](./docs/console.png?raw=true "Console output")
