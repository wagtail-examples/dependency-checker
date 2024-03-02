import os
import pathlib
import subprocess

import pytest
from src.managers.repository import RepositoryManager


@pytest.fixture
def repo(tmpdir):
    dir = os.path.dirname(os.path.abspath(__file__))
    pyproject_content = open(pathlib.Path(dir).joinpath("file_fixtures/pyproject.txt"), "r").read()
    dockerfile_content = open(pathlib.Path(dir).joinpath("file_fixtures/docker.txt"), "r").read()

    t = tmpdir.mkdir("repo")
    t.join("pyproject.toml").write(pyproject_content)
    t.join("Dockerfile").write(dockerfile_content)

    os.chdir(t)
    subprocess.run(["git", "config", "--global", "user.email", "user@example.com"], check=True, capture_output=True)
    subprocess.run(["git", "config", "--global", "user.name", "user"], check=True, capture_output=True)
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], check=True, capture_output=True)
    subprocess.run(["git", "checkout", "master"], check=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "test"], check=True, capture_output=True)
    path = pathlib.Path(t)
    return path


@pytest.fixture
def repository_manager(repo):
    return RepositoryManager(repo_url=repo, docker_file_name="Dockerfile")
