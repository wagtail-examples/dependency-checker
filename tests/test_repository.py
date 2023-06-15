import pytest
import subprocess
from src.managers.repository import RepositoryManager
from unittest.mock import patch


def test_repository_manager(repo_fixture):
    manager = RepositoryManager(repo_fixture)
    manager.clone()
    assert manager.repo_dir is not None
    assert manager.repo_dir.exists()

    with subprocess.Popen(
        ["git", "status"], cwd=manager.repo_dir, stdout=subprocess.PIPE
    ) as proc:
        assert b"On branch main" in proc.stdout.read()

    manager.branch("test-branch")

    with subprocess.Popen(
        ["git", "status"], cwd=manager.repo_dir, stdout=subprocess.PIPE
    ) as proc:
        assert b"On branch test-branch" in proc.stdout.read()

    assert manager.toml_exists()
    assert manager.toml is not None
    # assert manager.requirements_exists()
    # assert manager.get_requirements is not None
    assert manager.dockerfile_exists()
    assert manager.get_dockerfile is not None
    assert manager.docker_image == "python:3.8-buster"
    assert manager.poetry_version == "1.4.2"

    manager.branch("main")

    with subprocess.Popen(
        ["git", "status"], cwd=manager.repo_dir, stdout=subprocess.PIPE
    ) as proc:
        assert b"On branch main" in proc.stdout.read()

    manager.remove_temp_dir()
    assert not manager.repo_dir.exists()


def test_repository_manager_clone_error(repo_fixture):
    with pytest.raises(SystemExit) as e:
        manager = RepositoryManager(repo_fixture)
        manager.clone()
        manager.branch("test")
        assert e.value.code != 0
        assert "Error cloning repository" in e


def test_repository_manager_branch_error(repo_fixture):
    with pytest.raises(SystemExit) as e:
        manager = RepositoryManager(repo_fixture)
        manager.clone()
        manager.branch("test")
        assert e.value.code != 0
        assert "Error checking out branch" in e
