import pathlib

import click
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from src.client import PyPiClient
from src.managers.docker import DockerManager
from src.managers.package import Package
from src.managers.repository import RepositoryManager
from src.parsers.text import TextParser
from src.parsers.toml import TomlParser
from src.reporters.html import HTMLReporter

console = Console()
reporter = HTMLReporter()


@click.command()
@click.option(
    "--repo-url",
    prompt="Repository URL",
    help="The URL of the repository to clone.",
)
@click.option(
    "--report",
    "-r",
    is_flag=True,
    help="Generate a report of the dependencies.",
)
def start(repo_url, report):
    console.clear()
    console.print("Welcome to the Dependency Checker.", style="bright_white")
    console.print(
        "This tool will help you analyze the python dependencies used in a Docker image.", style="bright_white"
    )
    console.print("Please wait while we process the repository ...", style="cyan1")

    client = PyPiClient()

    # clone the repository
    repository_manager = RepositoryManager(repo_url)

    branches = repository_manager.get_branches()
    console.print("")
    console.print("Available branches:", style="yellow1")

    column_data = []
    for branch in branches.items():
        if branch[0] < 10:
            column_data.append(f" {branch[0]} {branch[1]}")
        else:
            column_data.append(f"{branch[0]} {branch[1]}")
    columns = Columns(column_data, equal=True, expand=True, column_first=True, padding=(0, 0))
    console.print(columns)

    console.print("")
    choice = console.input("Enter the branch number of the branch you'd like to analyse: ")
    if not choice or int(choice) not in branches:
        console.print("Invalid branch number.", style="red1")
        exit()
    branch_name = branches[int(choice)]
    repository_manager.change_branch(branch_name)

    console.clear()

    docker_files = repository_manager.find_docker_files()

    if len(docker_files) == 0:
        console.print("No Dockerfile found in the repository.", style="red1")
        exit()

    if len(docker_files) > 1:
        choices = [f"{i}. {docker_file.name}" for i, docker_file in enumerate(docker_files, 1)]
        choices = "\n".join(choices)
        choice = console.input(f"Multiple Dockerfiles found. Please choose one:\n{choices}\n")
        repository_manager.dockerfile_path = str(pathlib.Path(docker_files[int(choice) - 1]).absolute())
    else:
        repository_manager.dockerfile_path = str(pathlib.Path(docker_files[0]).absolute())

    repository_manager.parse_docker_image()
    repository_manager.parse_poetry_version()

    table = Table(title="Repository Information", box=box.MARKDOWN, show_lines=True)
    table.add_column("", style="bright_white")
    table.add_column("Details", style="bright_white")
    table.add_row("Repository URL", repository_manager.repo_url)
    table.add_row("Branch Name", repository_manager.get_branch())
    table.add_row("Dockerfile Path", repository_manager.dockerfile_path)
    table.add_row("Poetry Version", repository_manager.poetry_version)
    table.add_row("Docker Image", repository_manager.docker_image)
    console.print(table)

    process = click.confirm("Do you want to continue with the above details?", default=True)

    console.clear()

    if not process:
        console.print("Exiting ...", style="red1")
        exit()

    # run the docker image
    docker = DockerManager(
        repository_manager.docker_image,
        repository_manager.poetry_version,
        repository_manager.get_repo_dir,
    )

    docker.generate_run_command()
    docker.generate_bash_command()

    console.print(
        f"The command below will be used to run a docker container:\n\n{docker.run_cmd} '{docker.bash_cmd}'\n",
        style="bright_white",
    )
    process = click.confirm("Do you want to continue with the above command?", default=True)

    console.clear()

    if not process:
        console.print("Exiting ...", style="red1")
        exit()

    console.print("Running the docker image. This may take some time ...", style="yellow1")
    docker.run()

    console.clear()

    console.print("")
    table = Table(title="Repository Information", box=box.MARKDOWN, show_lines=True)
    table.add_column("", style="bright_white")
    table.add_column("Details", style="bright_white")
    table.add_row("Repository URL", repository_manager.repo_url)
    table.add_row("Branch Name", repository_manager.get_branch())
    table.add_row("Dockerfile Path", repository_manager.dockerfile_path)
    table.add_row("Poetry Version", repository_manager.poetry_version)
    table.add_row("Docker Image", repository_manager.docker_image)
    console.print(table)

    if report:
        reporter.add_info_data(
            {
                "Repository URL": repository_manager.repo_url,
                "Branch Name": repository_manager.get_branch(),
                "Dockerfile Path": repository_manager.dockerfile_path,
                "Poetry Version": repository_manager.poetry_version,
                "Docker Image": repository_manager.docker_image,
            }
        )

    console.print("Analyzing the dependencies ...", style="cyan1")

    # process the requirements-frozen.txt file as a FrozenParser object
    # it's used to lookup the package name and version installed in the docker image
    frozen = TextParser(pathlib.Path(repository_manager.get_repo_dir / "requirements-frozen.txt").absolute())

    # process the pyproject.toml file as a TomlParser object
    # it's used to lookup the package name and version specified in the pyproject.toml file
    toml = TomlParser(pathlib.Path(repository_manager.get_repo_dir).absolute() / "pyproject.toml")

    dependencies = sorted(toml.dependencies.keys())
    dev_dependencies = sorted(toml.dev_dependencies.keys())

    messages = []

    production_packages = []
    development_packages = []

    # production dependencies
    console.print("")
    table = Table(title="Production Dependencies", box=box.MARKDOWN, show_lines=True)
    table.add_column("Package", style="bright_white")
    table.add_column("Installed Version", style="bright_white")
    table.add_column("Latest Version", style="bright_white")
    table.add_column("Status", style="bright_white")

    for dependency in dependencies:
        c = client.get_package(dependency)
        if isinstance(c, int):
            # deals with cases such as package names with [extras] in them
            messages.append(f"{dependency}")
            continue
        package = Package(c.json())

        production_packages.append(package)

    for package in production_packages:
        name = package.name
        latest_version = package.latest_version
        frozen_version = frozen.dependencies.get(name.lower())
        if frozen_version and frozen_version != latest_version:
            if "git+https://" in frozen_version:
                status = "Check"
                style = "red1"
            else:
                status = "Outdated"
                style = "yellow1"
        elif not frozen_version:
            status = "Check"
            style = "cyan1"
            frozen_version = "Unable to determine version"
        else:
            status = "OK"
            style = "green3"

        if "git+https://" in frozen_version:
            frozen_version = frozen_version.replace("git+https://", "")
            frozen_version = f"{frozen_version.split('@')[0]} TAG {frozen_version.split('@')[1]}"

        table.add_row(name, frozen_version, latest_version, status, style=style)

        if report:
            reporter.add_production_data(
                {
                    "Package": name,
                    "Installed Version": frozen_version,
                    "Latest Version": latest_version,
                    "Status": status,
                }
            )

    console.print(table)

    # development dependencies
    console.print("\n")
    table = Table(title="Development Dependencies", box=box.MARKDOWN, show_lines=True)
    table.add_column("Package", style="bright_white")
    table.add_column("Installed Version", style="bright_white")
    table.add_column("Latest Version", style="bright_white")
    table.add_column("Status", style="bright_white")

    # development dependencies
    for dependency in dev_dependencies:
        c = client.get_package(dependency)
        if isinstance(c, int):
            # deals with cases such as package names with [extras] in them
            messages.append(f"{dependency}")
            continue

        package = Package(c.json())

        development_packages.append(package)

    for package in development_packages:
        name = package.name
        latest_version = package.latest_version
        frozen_version = frozen.dependencies.get(name.lower())
        if frozen_version and frozen_version != latest_version:
            if "git+https://" in frozen_version:
                status = "Check"
                style = "bright_red"
            else:
                status = "Outdated"
                style = "bright_yellow"
        elif not frozen_version:
            status = "Check"
            style = "magenta"
            frozen_version = "Unable to determine version"
        else:
            status = "OK"
            style = "bright_green"

        table.add_row(name, frozen_version, latest_version, status, style=style)

        if report:
            reporter.add_development_data(
                {
                    "Package": name,
                    "Installed Version": frozen_version,
                    "Latest Version": latest_version,
                    "Status": status,
                }
            )

    console.print(table)

    reporter.write_report()
