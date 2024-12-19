import pathlib

import click
from src.check_local import check_local
from src.check_remote import check_remote


@click.group()
@click.version_option(version="0.1.0", prog_name="Python Dependency Checker")
@click.option("--report", "-r", is_flag=True, help="Generate a printable report.")
@click.pass_context
def cli(ctx: click.Context, report: bool):
    """Python Dependency Checker CLI tool."""
    ctx.ensure_object(dict)
    ctx.obj["report"] = report


@cli.command()
@click.option("--repo-url", prompt="Repository URL", help="The URL of the repository to clone.")
@click.pass_context
def remote(ctx: click.Context, repo_url: str):
    """Analyze the dependencies of a remote repository"""
    check_remote(repo_url, ctx.obj["report"])


@cli.command()
@click.argument(
    "path",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
@click.pass_context
def local(ctx: click.Context, path: pathlib.Path):
    """Analyze the dependencies of a local repository"""
    check_local(path, ctx.obj["report"])
