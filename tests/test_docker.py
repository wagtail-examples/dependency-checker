from unittest.mock import patch

from src.managers.docker import DockerManager


@patch("subprocess.run")
def test_docker_manager_instance(mock_subprocess_run):
    docker_manager = DockerManager(
        "python",
        "3.9.7",
        "repo_dir",
    )

    assert docker_manager.image == "python"
    assert docker_manager.poetry_version == "3.9.7"
    assert docker_manager.repo_dir == "repo_dir"
    assert docker_manager.docker_run_name == "poetry-export"

    docker_manager.generate_run_command()
    assert (
        docker_manager.run_cmd
        == "docker run --name poetry-export -it --rm --volume repo_dir:/app -w /app python bash -c"
    )

    docker_manager.generate_bash_command()
    assert (
        docker_manager.bash_cmd
        == "pip install -U pip && pip install poetry==3.9.7 && poetry export -f requirements.txt -o requirements-frozen.txt --without-hashes --dev"  # noqa: E501
    )

    docker_manager.run()
    mock_subprocess_run.assert_called_with(
        f"{docker_manager.run_cmd} '{docker_manager.bash_cmd}'", shell=True, check=True, cwd="repo_dir"
    )

    docker_manager.run("run_cmd", "bash_cmd")
    mock_subprocess_run.assert_called_with("run_cmd 'bash_cmd'", shell=True, check=True, cwd="repo_dir")
