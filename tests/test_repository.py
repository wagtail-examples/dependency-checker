import os
import pathlib

from src.managers.repository import RepositoryManager


def test_repository_manager_init(repo_content):
    repo = RepositoryManager(repo_content)
    repo_path = pathlib.Path(__file__).parent.parent / repo.repo_dir.name

    assert repo.repo_url == repo_content
    # assert repo.dockerfile_name == ""
    # assert repo.dockerfile_path == "./"

    # Test that the repository was cloned and the path is correct
    assert pathlib.Path(repo.repo_dir.name) == repo_path.absolute()

    # Test that these files exist
    os.chdir(repo.repo_dir.name)
    assert os.path.exists("pyproject.toml")
    assert os.path.exists("Dockerfile")
    assert os.path.exists(".git")
    assert repo.get_branch() == "main"

    # Test change branch
    assert repo.change_branch("test") == "branch 'test' set up to track 'origin/test'."

    # Test nonexistent branch
    assert (
        repo.change_branch("nonexistent")
        == "Error: Branch nonexistent does not exist in the repository. Please check the branch name and try again."
    )

    # Test can find Dockerfile and return path
    # print(repo.find_docker_files())
    assert repo.find_docker_files() == [repo_path / "Dockerfile"]

    # Duplicate the Dockerfile and test that it can still be found
    os.system(f"cp {repo_path / 'Dockerfile'} {repo_path / 'Dockerfile2'}")
    os.system(f"cp {repo_path / 'Dockerfile'} {repo_path / 'Dockerfile3'}")
    # Create one in a sub folder
    os.system(f"mkdir {repo_path / 'sub_folder'}")
    os.system(f"cp {repo_path / 'Dockerfile'} {repo_path / 'sub_folder/Dockerfile4'}")

    assert len(repo.find_docker_files()) == 4
    assert repo.find_docker_files()[0] == repo_path / "Dockerfile"
    assert repo.find_docker_files()[1] == repo_path / "Dockerfile3"
    assert repo.find_docker_files()[2] == repo_path / "Dockerfile2"
    assert repo.find_docker_files()[3] == repo_path / "sub_folder/Dockerfile4"

    repo.dockerfile_path = repo.find_docker_files()[0]
    repo.parse_docker_image()
    assert repo.docker_image == "python:3.11-slim-bullseye"

    repo.parse_poetry_version()
    assert repo.poetry_version == "1.3.2"

    # Test no Dockerfile found
    os.remove(repo_path / "Dockerfile")
    os.remove(repo_path / "Dockerfile2")
    os.remove(repo_path / "Dockerfile3")
    os.remove(repo_path / "sub_folder/Dockerfile4")
    assert repo.find_docker_files() == []


# import subprocess


# def test_repository_manager_init(repository_manager, repo):
#     assert repository_manager.repo_url == repo
#     assert repository_manager.docker_file_name == "Dockerfile"
#     assert repository_manager.temp_dir is not None
#     assert "docker-run-" in repository_manager.temp_dir.name


# def test_repository_manager_clone(repository_manager):
#     repository_manager.clone()
#     assert repository_manager.repo_dir.exists()


# # def test_repository_manager_branch(repository_manager):
# #     repository_manager.clone()
# #     # switch to the test branch and check that it exists
# #     repository_manager.branch("test")
# #     assert (
# #         subprocess.run(
# #             ["git", "branch"], cwd=repository_manager.repo_dir, check=True, capture_output=True
# #         ).stdout.decode("utf-8")
# #         == "* test\n"
# #     )


# def test_toml_exists(repository_manager):
#     repository_manager.clone()
#     assert repository_manager.toml_exists()


# def test_dockerfile_exists(repository_manager):
#     repository_manager.clone()
#     assert repository_manager.dockerfile_exists()


# # def test_docker_image(repository_manager):
# #     repository_manager.clone()
# #     assert repository_manager.docker_image == "python:3.9-buster"


# # def test_poetry_version(repository_manager):
# #     repository_manager.clone()
# #     assert repository_manager.poetry_version == "1.1.4"
