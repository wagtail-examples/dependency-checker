import os
import pathlib
import subprocess

import pytest
from click.testing import CliRunner
from src.main import start
from src.managers.repository import RepositoryManager


@pytest.fixture
def repo(tmpdir):
    t = tmpdir.mkdir("repo")
    pyproject_content = "[tool.poetry]\nname = 'test'\nversion = '0.1.0'\ndescription = 'test'\nauthors = ['test']\nlicense = 'MIT'\n[tool.poetry.dependencies]\npython = '^3.9'\nrequests = '^2.31.0'\n"  # noqa: E501
    t.join("pyproject.toml").write(pyproject_content)
    dockerfile_content = "FROM python:3.9-buster as production\nARG POETRY_VERSION=1.1.4\n"
    t.join("Dockerfile").write(dockerfile_content)

    os.chdir(t)
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], check=True, capture_output=True)
    subprocess.run(["git", "branch", "master"], check=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "test"], check=True, capture_output=True)
    path = pathlib.Path(t)
    return path


@pytest.fixture
def repository_manager(repo):
    return RepositoryManager(repo_url=repo, docker_file_name="Dockerfile")


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
