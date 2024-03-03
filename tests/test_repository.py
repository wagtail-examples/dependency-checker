# import subprocess


def test_repository_manager_init(repository_manager, repo):
    assert repository_manager.repo_url == repo
    assert repository_manager.docker_file_name == "Dockerfile"
    assert repository_manager.temp_dir is not None
    assert "docker-run-" in repository_manager.temp_dir.name


def test_repository_manager_clone(repository_manager):
    repository_manager.clone()
    assert repository_manager.repo_dir.exists()


# def test_repository_manager_branch(repository_manager):
#     repository_manager.clone()
#     # switch to the test branch and check that it exists
#     repository_manager.branch("test")
#     assert (
#         subprocess.run(
#             ["git", "branch"], cwd=repository_manager.repo_dir, check=True, capture_output=True
#         ).stdout.decode("utf-8")
#         == "* test\n"
#     )


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
