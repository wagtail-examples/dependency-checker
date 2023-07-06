# Dependency version checker for Python

![Icon](./docs/icon.png?raw=true "Icon")

## Installation

Clone this repository and run the following commands in the root of the project:

## Usage

```bash
poetry install
poetry run start
```

Enter the url for your repository and set any options where the default isn't correct.

## Options

Options can be passed in as command line arguments or enter them when prompted.

```bash
poetry run start --help
```

- `--repo-url` - The URL of the repository to clone/check
- `--branch-name` - The branch to checkout [master]
- `--docker-file-name` - The name of the Dockerfile to inspect/use [Dockerfile]
- `--docker-file-location` - The location of the Dockerfile to inspect/use relative to the repository root [./]


## Limitations

- Only works if the Dockerfile uses poetry to install dependencies

## TODO

- Add support for different dependency managers (requirements.txt, etc.)

## How it works

- It will clone the repository and checkout the specified branch
- It will then inspect the Dockerfile to find the image version and poetry version used
- It will then build a new image based on the Dockerfile image and export the dependency list using poetry export -> requirements-frozen.txt
- It will then compare each dependency version in requirements-frozen.txt with the latest version on PyPi
- It will then output the results in the console and indicate if there are any outdated dependencies and/or manual checks required

e.g. Console output

![Console ouput](./docs/console.png?raw=true "Console output")
