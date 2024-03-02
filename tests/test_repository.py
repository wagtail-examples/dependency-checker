import os
import pathlib
import subprocess

import pytest
from src.managers.repository import RepositoryManager


@pytest.fixture
def repo(tmpdir):
    t = tmpdir.mkdir("repo")
    pyproject_content = "[tool.poetry]\nname = 'test'\nversion = '0.1.0'\ndescription = 'test'\nauthors = ['test']\nlicense = 'MIT'\n[tool.poetry.dependencies]\npython = '^3.9'\nrequests = '^2.31.0'\n"  # noqa: E501
    t.join("pyproject.toml").write(pyproject_content)
    dockerfile_content = "FROM python:3.9-buster as production\nARG POETRY_VERSION=1.1.4\n"
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


def test_repository_manager_init(repository_manager, repo):
    assert repository_manager.repo_url == repo
    assert repository_manager.docker_file_name == "Dockerfile"
    assert repository_manager.temp_dir is not None
    assert "docker-run-" in repository_manager.temp_dir.name


def test_repository_manager_clone(repository_manager):
    repository_manager.clone()
    assert repository_manager.repo_dir.exists()


def test_repository_manager_branch(repository_manager):
    repository_manager.clone()
    # switch to the test branch and check that it exists
    repository_manager.branch("test")
    assert (
        subprocess.run(
            ["git", "branch"], cwd=repository_manager.repo_dir, check=True, capture_output=True
        ).stdout.decode("utf-8")
        == "* test\n"
    )


def test_toml_exists(repository_manager):
    repository_manager.clone()
    assert repository_manager.toml_exists()


def test_dockerfile_exists(repository_manager):
    repository_manager.clone()
    assert repository_manager.dockerfile_exists()


def test_docker_image(repository_manager):
    repository_manager.clone()
    assert repository_manager.docker_image == "python:3.9-buster"


def test_poetry_version(repository_manager):
    repository_manager.clone()
    assert repository_manager.poetry_version == "1.1.4"
