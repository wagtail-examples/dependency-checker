import os
import pathlib
import subprocess

import pytest
from src.managers.repository import RepositoryManager


@pytest.fixture()
def repo(tmpdir):
    dir = pathlib.Path(tmpdir)
    base_dir = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

    pyproject_content = open(pathlib.Path(base_dir).joinpath("file_fixtures/pyproject.txt"), "r").read()
    dockerfile_content = open(pathlib.Path(base_dir).joinpath("file_fixtures/docker.txt"), "r").read()

    os.chdir(dir)

    subprocess.run(["git", "config", "--global", "user.email", "user@example.com"], check=True, capture_output=True)
    subprocess.run(["git", "config", "--global", "user.name", "user"], check=True, capture_output=True)
    subprocess.run(["git", "config", "--global", "init.defaultBranch", "master"], check=True, capture_output=True)
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["touch", "pyproject.toml"], check=True, capture_output=True)
    subprocess.run(["touch", "Dockerfile"], check=True, capture_output=True)

    with open(os.path.join(dir, "pyproject.toml"), "w") as f:
        f.write(pyproject_content)
    with open(os.path.join(dir, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)

    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add files"], check=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "test"], check=True, capture_output=True)

    return dir


@pytest.fixture
def repository_manager(repo):
    return RepositoryManager(repo_url=repo, docker_file_name="Dockerfile")
