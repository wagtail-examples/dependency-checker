import pathlib

import click
from rich import box
from rich.console import Console
from rich.table import Table
from src.managers.package import Client, Package
from src.managers.repository import RepositoryManager
from src.managers.runner import DockerManager
from src.parsers.text import TextParser
from src.parsers.toml import TomlParser

console = Console()


# @click.option(
#     "--docker-file-name",
#     prompt="Dockerfile name (optional)",
#     help="The name of the Dockerfile to use.",
#     default="Dockerfile",
# )
# @click.option(
#     "--docker-file-location",
#     prompt="Dockerfile relative location (optional)",
#     help="The location of the Dockerfile to use relative to the root.",
#     default="./",
# )
@click.command()
@click.option(
    "--repo-url",
    prompt="Repository URL",
    help="The URL of the repository to clone.",
)
@click.option(
    "--branch-name",
    prompt="Branch name (optional)",
    help="The name of the branch to checkout.",
    default="master",
)
def start(
    repo_url,
    branch_name,
):
    client = Client("https://pypi.org/pypi")

    # clone the repository
    repository_manager = RepositoryManager(repo_url)

    if repository_manager.get_branch() != branch_name:
        result = repository_manager.change_branch(branch_name)
        if "Error" in result:
            console.print(result, style="red1")
            exit()

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

    console.print("\n")
    table = Table(title="Repository Information", box=box.MARKDOWN, show_lines=True)
    table.add_column("", style="bright_white")
    table.add_column("Details", style="bright_white")
    # table.add_column("Repository URL", style="bright_white")
    # table.add_column("Branch Name", style="bright_white")
    # table.add_column("Dockerfile Path", style="bright_white")
    # table.add_row(repository_manager.repo_url, repository_manager.get_branch(), repository_manager.dockerfile_path)
    table.add_row("Repository URL", repository_manager.repo_url)
    table.add_row("Branch Name", repository_manager.get_branch())
    table.add_row("Dockerfile Path", repository_manager.dockerfile_path)
    table.add_row("Poetry Version", repository_manager.poetry_version)
    table.add_row("Docker Image", repository_manager.docker_image)
    console.print(table)

    process = click.confirm("Do you want to continue with the above details?", default=True)

    if not process:
        console.print("Exiting ...", style="red1")
        exit()

    console.print("\n")
    console.print("Running the docker image. This may take some time ...", style="yellow1")

    # table.add_row(repository_manager.repo_url)
    # table.add_row(repository_manager.get_branch())
    # table.add_row(repository_manager.dockerfile_path)
    # table.add_row(repository_manager.poetry_version)
    # table.add_row(repository_manager.docker_image)

    # print(repository_manager.docker_image)
    # print(repository_manager.poetry_version)
    # print(repository_manager.poetry_version)

    # exit()
    # exit()
    # exit()
    # if not docker_file_location == "./":
    #     df = f"{docker_file_location}/{docker_file_name}"
    #     repo_manager = RepositoryManager(repo_url, df)
    # else:
    #     repo_manager = RepositoryManager(repo_url, docker_file_name)

    # repo_manager.clone()
    # switch to an alternative branch if specified
    # repo_manager.branch(branch_name)
    # get the docker image from the Dockerfile
    # docker_image = repository_manager.docker_image
    # get the poetry version from the Dockerfile
    # poetry_latest_version = client.get("poetry").json()["info"]["version"]

    # console.print("\n")
    # table = Table(title="Docker Information", box=box.MARKDOWN, show_lines=True)
    # table.add_column("Docker Image", style="bright_white")
    # table.add_column("Poetry Version", style="bright_white")
    # table.add_column("Latest Poetry Version", style="bright_white")
    # table.add_row(docker_image, poetry_version, poetry_latest_version)
    # console.print(table)

    # exit()

    # run the docker image
    docker = DockerManager(docker_image, poetry_version, repo_manager.repo_dir)  # noqa
    console.print("Running the docker image. This may take some time ...", style="yellow1")
    docker.run(docker.run_cmd, docker.run_args)

    # process the requirements-frozen.txt file as a FrozenParser object
    # it's used to lookup the package name and version installed in the docker image
    frozen = TextParser()
    frozen.parse_requirements()
    frozen_dependencies = frozen.requirements

    # process the pyproject.toml file as a TomlParser object
    # it's used to lookup the package name and version specified in the pyproject.toml file
    toml = TomlParser(repo_manager.toml)  # noqa
    dependencies = sorted(toml.dependencies().keys())
    dev_dependencies = sorted(toml.dev_dependencies().keys())

    messages = []

    production_packages = []
    development_packages = []

    # production dependencies
    console.print("\n")
    table = Table(title="Production Dependencies", box=box.MARKDOWN, show_lines=True)
    table.add_column("Package", style="bright_white")
    table.add_column("Installed Version", style="bright_white")
    table.add_column("Latest Version", style="bright_white")
    table.add_column("Status", style="bright_white")

    for dependency in dependencies:
        c = client.get(dependency)
        if isinstance(c, int):
            # deals with cases such as package names with [extras] in them
            messages.append(f"{dependency}")
            continue
        package = Package(c.json())

        production_packages.append(package)

    for package in production_packages:
        name = package.name
        latest_version = package.latest_version
        frozen_version = frozen_dependencies.get(name.lower())
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
        c = client.get(dependency)
        if isinstance(c, int):
            # deals with cases such as package names with [extras] in them
            messages.append(f"{dependency}")
            continue

        package = Package(c.json())

        development_packages.append(package)

    for package in development_packages:
        name = package.name
        latest_version = package.latest_version
        frozen_version = frozen_dependencies.get(name.lower())
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

    console.print(table)

    # cleanup
    frozen.clean_up_frozen()
    docker.cleanup_docker()
