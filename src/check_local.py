import pathlib

import click
from rich.columns import Columns
from rich.console import Console
from src.helpers import (
    dependency_table_header,
    get_branch_data,
    get_packages,
    information_table,
    package_table_row,
)
from src.managers.docker import DockerManager
from src.managers.repository import RepositoryManagerLocal as RepositoryManager
from src.parsers.text import TextParser
from src.parsers.toml import TomlParser
from src.reporters.html import HTMLReporter


def check_local(path: str, report: bool) -> None:
    rich_console = Console()
    html_reporter = HTMLReporter()

    rich_console.clear()
    rich_console.print("Analysing the repository...", style="cyan1")

    # clone the repository
    repository_manager = RepositoryManager(path)

    # get and display the available branches
    branches = repository_manager.get_branches()

    rich_console.print("Available branches:", style="yellow1", new_line_start=True)
    rich_console.print(Columns(get_branch_data(branches), equal=True, expand=True, column_first=True, padding=(0, 0)))

    # choose a branch name by index
    choice = rich_console.input("Enter the branch number of the branch you'd like to analyse: ")
    if not choice or int(choice) not in branches:
        rich_console.print("Invalid branch number.", style="red1")
        exit()
    branch_name = branches[int(choice)]
    repository_manager.change_branch(branch_name)

    # find the docker files in the repository
    docker_files = repository_manager.find_docker_files()

    if len(docker_files) == 0:
        # exit if no Dockerfile is found
        rich_console.print("No Dockerfile found in the repository.", style="red1")
        exit()

    if len(docker_files) > 1:
        # choose a Dockerfile if multiple are found
        choices = [f"{i}. {docker_file.name}" for i, docker_file in enumerate(docker_files, 1)]
        choices = "\n".join(choices)
        choice = rich_console.input(f"Multiple Dockerfiles found. Please choose one:\n{choices}\n")
        repository_manager.dockerfile_path = str(pathlib.Path(docker_files[int(choice) - 1]).absolute())
    else:
        # use the only Dockerfile found
        repository_manager.dockerfile_path = str(pathlib.Path(docker_files[0]).absolute())

    # parse the Dockerfile to get the base image
    repository_manager.parse_docker_image()
    docker_image = repository_manager.docker_image

    if not docker_image:
        # prompt for a Docker image if not found or it cannot be parsed
        rich_console.print("Unable to determine the base image from the Dockerfile.", style="red1")
        docker_image = click.prompt("Enter a valid Docker image to use e.g. python:3.11", type=str)

    # we need the version to install poetry the same version in the Docker image
    # the same version may not be required but doing it anyway
    repository_manager.parse_poetry_version()
    poetry_version = repository_manager.poetry_version

    if not poetry_version:
        rich_console.print("Unable to determine the poetry version from the Dockerfile.", style="red1")
        poetry_version = click.prompt("Enter a valid Poetry version to use e.g. 1.8.2", type=str)

    rich_console.print(information_table(repository_manager, docker_image, poetry_version), new_line_start=True)

    process = click.confirm("Do you want to continue with the above details?", default=True)

    if not process:
        rich_console.print("Exiting ...", style="red1")
        exit()

    # run the docker image
    docker = DockerManager(docker_image, poetry_version, repository_manager.get_repo_dir)

    rich_console.print(
        f"Build & run a docker container with the following command:\n\n{docker.run_cmd}\n'{docker.bash_cmd}'\n",
        style="bright_white",
        new_line_start=True,
    )
    process = click.confirm("Do you want to continue with the above command?", default=True)

    rich_console.clear()

    if not process:
        rich_console.print("Exiting ...", style="red1")
        exit()

    rich_console.print("Build & run the docker image. This may take some time ...", style="yellow1")
    docker.run()

    rich_console.clear()

    rich_console.print("Analyzing the dependencies ...", style="cyan1")

    # process the requirements-frozen.txt file as a FrozenParser object
    # it's used to lookup the package name and version installed in the docker image
    requirements_file = pathlib.Path(repository_manager.get_repo_dir / "requirements-frozen.txt").absolute()
    frozen = TextParser(requirements_file)

    # delete the requirements-frozen.txt file
    requirements_file.unlink()

    # process the pyproject.toml file as a TomlParser object
    # it's used to lookup the package name and version specified in the pyproject.toml file
    toml = TomlParser(pathlib.Path(repository_manager.get_repo_dir).absolute() / "pyproject.toml")

    messages = []

    # production dependencies
    dependencies = sorted(toml.dependencies.keys())
    table = dependency_table_header(title="Production Dependencies")

    production_packages = get_packages(dependencies, messages)

    for package in production_packages:
        name, latest_version, frozen_version, status, style = package_table_row(frozen, package)

        table.add_row(name, frozen_version, latest_version, status, style=style)

        if report:
            html_reporter.add_production_data(
                {
                    "Package": name,
                    "Installed Version": frozen_version,
                    "Latest Version": latest_version,
                    "Status": status,
                }
            )

    rich_console.print(table, new_line_start=True)

    # development dependencies
    dev_dependencies = sorted(toml.dev_dependencies.keys())
    table = dependency_table_header(title="Development Dependencies")

    development_packages = get_packages(dev_dependencies, messages)

    for package in development_packages:
        name, latest_version, frozen_version, status, style = package_table_row(frozen, package)

        table.add_row(name, frozen_version, latest_version, status, style=style)

        if report:
            html_reporter.add_development_data(
                {
                    "Package": name,
                    "Installed Version": frozen_version,
                    "Latest Version": latest_version,
                    "Status": status,
                }
            )

    rich_console.print(table, new_line_start=True)

    rich_console.print(information_table(repository_manager, docker_image, poetry_version))

    if report:
        html_reporter.add_info_data(
            {
                "Repository URL": repository_manager.repo_url,
                "Branch Name": repository_manager.get_branch(),
                "Dockerfile Path": repository_manager.dockerfile_path,
                "Poetry Version": repository_manager.poetry_version,
                "Docker Image": repository_manager.docker_image,
            }
        )
        html_reporter.write_report()
