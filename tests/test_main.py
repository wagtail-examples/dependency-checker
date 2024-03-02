import pytest
from click.testing import CliRunner
from src.main import start


@pytest.fixture
def runner():
    return CliRunner()


def test_start(runner, repo):
    # Simulate a command-line invocation with the desired options
    result = runner.invoke(
        start,
        [
            "--repo-url",
            repo,
            "--branch-name",
            "test",
            "--docker-file-name",
            "Dockerfile",
            "--docker-file-location",
            "./",
        ],
        input="\n",  # Simulate user input (pressing Enter)
    )

    # Assert the expected output
    assert "Cloning repository" in result.output
    assert "Cloned repository to" in result.output
    assert "Checked out branch" in result.output
    assert "Found Docker image" in result.output
    assert "Found Poetry version" in result.output
    assert "Running the docker image. This may take some time ..." in result.output


def test_start_defaults(runner, repo):
    # Simulate a command-line invocation with the desired options
    result = runner.invoke(
        start,
        [
            "--repo-url",
            repo,
        ],
        input="\n",  # Simulate user input (pressing Enter)
    )

    # Assert the expected output
    assert "Cloning repository" in result.output
    assert "Cloned repository to" in result.output
    assert "Checked out branch" in result.output
    assert "Found Docker image" in result.output
    assert "Found Poetry version" in result.output
    assert "Running the docker image. This may take some time ..." in result.output
