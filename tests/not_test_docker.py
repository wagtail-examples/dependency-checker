# from src.managers.docker import DockerManager

# def test_docker_manager(repo_content):
#     docker_manager = DockerManager(
#         "python:3.9.7-slim-buster",
#         "1.7.1",
#         repo_content,
#     )

#     run_command = docker_manager.run_cmd()
#     assert (
#         "docker run --name poetry-export -it --rm --volume "
#         f"{repo_content}:/app -w /app python:3.9.7-slim-buster bash -c" in run_command
#     )

#     bash_command = docker_manager.bash_cmd()
#     assert (
#         "pip install -U pip && pip install poetry==1.7.1 && poetry export -f requirements.txt -o requirements-frozen.txt --without-hashes --dev"  # noqa
#         in bash_command
#     )

#     run_result = docker_manager.run(
#         run_command,
#         bash_command,
#     )

#     print(run_result)  # noqa


# @pytest.fixture
# def docker_manager(tmpdir):
#     return DockerManager(
#         "python",
#         "3.9.7",
#         tmpdir,
#     )


# def test_docker_manager(docker_manager):
#     assert docker_manager.get_docker_image == "python"
#     assert docker_manager.run_cmd == (
#         "docker run --name poetry-export -it --volume " f"{docker_manager.repo_dir}:/app -w /app python bash -c"
#     )
#     assert docker_manager.run_args == (
#         "pip install -U pip && pip install poetry==3.9.7 && "
#         "poetry export -f requirements.txt -o requirements-frozen.txt "
#         "--without-hashes --dev"
#     )
