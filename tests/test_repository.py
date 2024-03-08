import os
import pathlib

from src.managers.repository import RepositoryManager


def test_repository_manager_init(repo_content):
    repo = RepositoryManager(repo_content)
    repo_path = pathlib.Path(__file__).parent.parent / repo.repo_dir.name

    assert repo.repo_url == repo_content

    # Test that the repository was cloned and the path is correct
    assert pathlib.Path(repo.repo_dir.name) == repo_path.absolute()

    # Test that these files exist
    os.chdir(repo.repo_dir.name)
    assert os.path.exists("pyproject.toml")
    assert os.path.exists("Dockerfile")
    assert os.path.exists(".git")
    assert repo.get_branch() == "main"

    assert repo.get_repo_dir == repo_path

    # Test get branches
    assert repo.get_branches() == {1: "HEAD -> main", 2: "main ( DEFAULT )", 3: "test"}

    # Test change branch
    assert repo.change_branch("test") == "branch 'test' set up to track 'origin/test'."

    # Test nonexistent branch
    assert (
        repo.change_branch("nonexistent")
        == "Error: Branch nonexistent does not exist in the repository. Please check the branch name and try again."
    )

    repo.dockerfile_path = repo.find_docker_files()[0]
    repo.parse_docker_image()
    assert repo.docker_image == "python:3.11-slim-bullseye"

    repo.parse_poetry_version()
    assert repo.poetry_version == "1.3.2"
