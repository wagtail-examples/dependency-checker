import click


def check_local(path: str, report: bool) -> None:
    click.echo(f"Checking local repository at {path}...")
