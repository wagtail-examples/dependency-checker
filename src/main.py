import click
from src.check_local import check_local
from src.check_remote import check_remote


@click.group()
def cli():
    """Dependency Checker CLI tool."""


@cli.command()
@click.option(
    "--repo-url",
    prompt="Repository URL",
    help="The URL of the repository to clone.",
)
@click.option(
    "--report",
    "-r",
    is_flag=True,
    help="Generate a printable report.",
)
def remote(repo_url, report):
    """
    Analyze the dependencies of a remote repository.
    """

    check_remote(repo_url, report)


@cli.command()
@click.option(
    "--path",
    prompt="Path to the repository",
    help="The path to the repository to check.",
)
@click.option(
    "--report",
    "-r",
    is_flag=True,
    help="Generate a printable report.",
)
def local(path, report):
    """
    Analyze the dependencies of a local repository.
    """

    check_local(path, report)
