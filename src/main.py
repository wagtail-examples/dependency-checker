import click
from src.managers.package import Client, Package
from src.managers.repository import RepositoryManager
from src.managers.runner import DockerManager
from src.parsers.frozen import FrozenParser
from src.parsers.toml import TomlParser


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
@click.option(
    "--docker-file-name",
    prompt="Dockerfile name (optional)",
    help="The name of the Dockerfile to use.",
    default="Dockerfile",
)
@click.option(
    "--docker-file-location",
    prompt="Dockerfile relative location (optional)",
    help="The location of the Dockerfile to use relative to the root.",
    default="./",
)
def start(repo_url, branch_name, docker_file_name, docker_file_location=None):
    # clone the repository
    if not docker_file_location == "./":
        df = f"{docker_file_location}/{docker_file_name}"
        repo_manager = RepositoryManager(repo_url, df)
    else:
        repo_manager = RepositoryManager(repo_url, docker_file_name)

    click.echo(f"Cloning repository {repo_url} ...")
    repo_manager.clone()
    click.secho(f"Cloned repository to {repo_manager.repo_dir}")

    # switch to an alternative branch if specified
    # if branch_name != 'main':
    repo_manager.branch(branch_name)
    click.secho(f"Checked out branch {branch_name}")

    # get the docker image from the Dockerfile
    docker_image = repo_manager.docker_image
    click.secho(f"Found Docker image {docker_image}")

    # get the poetry version from the Dockerfile
    poetry_version = repo_manager.poetry_version
    click.secho(f"Found Poetry version {poetry_version}")

    # run the docker image
    docker = DockerManager(docker_image, poetry_version, repo_manager.repo_dir)
    click.echo("Running the docker image. This may take some time ...")
    docker.run(docker.run_cmd, docker.run_args)
    click.secho("Generated requirements-frozen.txt")

    # process the requirements-frozen.txt file as a FrozenParser object
    # it's used to lookup the package name and version installed in the docker image
    frozen = FrozenParser()
    click.echo("Processing frozen requirements ...")
    frozen.parse_requirements()
    frozen_dependencies = frozen.requirements

    # process the pyproject.toml file as a TomlParser object
    # it's used to lookup the package name and version specified in the pyproject.toml file
    toml = TomlParser(repo_manager.toml)
    click.echo("Processing pyproject.toml ...")
    dependencies = sorted(toml.dependencies().keys())
    dev_dependencies = sorted(toml.dev_dependencies().keys())

    report_production_dependencies = []
    report_dev_dependencies = []
    messages = []

    client = Client("https://pypi.org/pypi")

    click.echo("\n")
    click.secho("RED: Manual check should be carried out", fg="bright_red")
    click.secho("YELLOW: The latest available version is not installed", fg="bright_yellow")
    click.secho("GREEN: Using the latest version available is installed", fg="bright_green")

    # production dependencies
    click.echo("\n")
    click.secho("Production dependencies ...", **{"underline": True, "fg": "bright_white"})
    for dependency in dependencies:
        c = client.get(dependency)
        if isinstance(c, int):
            # deals with cases such as package names with [extras] in them
            messages.append(f"{dependency}")
            continue

        package = Package(c.json())
        latest_version = package.latest_version
        frozen_version = frozen_dependencies.get(dependency.lower())

        if frozen_version is None:
            # deals with cases such as package names that don't exist such as "python"
            messages.append(f"{dependency}")
            continue

        if frozen_version != latest_version:
            if "git+https://" not in frozen_version:
                report_production_dependencies.append(
                    (f"{dependency} {frozen_version} -> {latest_version}", "bright_yellow")
                )
            else:
                report_production_dependencies.append(
                    (f"{dependency} {frozen_version} -> {latest_version}", "bright_red")
                )
        else:
            report_production_dependencies.append((f"{dependency} == {frozen_version}", "bright_green"))

    if report_production_dependencies:
        for item in report_production_dependencies:
            click.secho(item[0], fg=item[1])

    # development dependencies
    click.echo("\n")
    click.secho("Development dependencies ...", **{"underline": True, "fg": "bright_white"})
    for dependency in dev_dependencies:
        c = client.get(dependency)
        if isinstance(c, int):
            # deals with cases such as package names with [extras] in them
            messages.append(f"{dependency}")
            continue

        package = Package(c.json())
        latest_version = package.latest_version
        frozen_version = frozen_dependencies.get(dependency.lower())

        if frozen_version is None:
            # deals with cases such as package names that don't exist such as "python"
            messages.append(f"{dependency}")
            continue

        if frozen_version != latest_version:
            if "git+https://" not in frozen_version:
                report_dev_dependencies.append((f"{dependency} {frozen_version} -> {latest_version}", "bright_yellow"))
            else:
                report_dev_dependencies.append((f"{dependency} {frozen_version} -> {latest_version}", "bright_red"))
        else:
            report_dev_dependencies.append((f"{dependency} == {frozen_version}", "bright_green"))

    if report_dev_dependencies:
        for item in report_dev_dependencies:
            click.secho(item[0], fg=item[1])

    if len(messages) > 0:
        click.secho("\n")
        click.secho("Manual check required", **{"underline": True, "fg": "bright_white"})
        for message in messages:
            click.secho(f"{message}", fg="bright_red")

    # cleanup
    frozen.clean_up_frozen()
    docker.cleanup_docker()
