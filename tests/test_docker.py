from unittest.mock import patch

from src.managers.docker import DockerManager


def test_docker_manager_instance_basic():
    """Test basic DockerManager instance attributes"""
    docker_manager = DockerManager(
        "python",
        "2.0.0",
        "repo_dir",
    )

    assert docker_manager.image == "python"
    assert docker_manager.poetry_version == "2.0.0"
    assert docker_manager.repo_dir == "repo_dir"
    assert docker_manager.docker_run_name == "poetry-export"


def test_docker_manager_run_command():
    """Test docker run command generation"""
    docker_manager = DockerManager(
        "python",
        "2.0.0",
        "repo_dir",
    )

    docker_manager.generate_run_command()
    assert (
        docker_manager.run_cmd
        == "docker run --name poetry-export -it --rm --volume repo_dir:/app -w /app python bash -c"
    )


def test_docker_manager_bash_command_poetry_1x():
    """Test bash command generation for Poetry 1.x"""
    docker_manager = DockerManager(
        "python",
        "1.8.0",
        "repo_dir",
    )

    docker_manager.generate_bash_command()
    assert (
        docker_manager.bash_cmd
        == "pip install -U pip && pip install poetry==1.8.0 && poetry export -f requirements.txt -o requirements-frozen.txt --without-hashes --dev"  # noqa: E501
    )


def test_docker_manager_bash_command_poetry_2x():
    """Test bash command generation for Poetry 2.x"""
    docker_manager = DockerManager(
        "python",
        "2.0.0",
        "repo_dir",
    )

    docker_manager.generate_bash_command()
    assert (
        docker_manager.bash_cmd
        == "pip install -U pip && pip install poetry==2.0.0 && pip install poetry-plugin-export && poetry export -f requirements.txt -o requirements-frozen.txt --without-hashes --with dev"  # noqa: E501
    )


@patch("subprocess.run")
def test_docker_manager_run(mock_subprocess_run):
    """Test docker manager run method"""
    docker_manager = DockerManager(
        "python",
        "2.0.0",
        "repo_dir",
    )

    docker_manager.run()
    mock_subprocess_run.assert_called_with(
        f"{docker_manager.run_cmd} '{docker_manager.bash_cmd}'", shell=True, check=True, cwd="repo_dir"
    )

    docker_manager.run("run_cmd", "bash_cmd")
    mock_subprocess_run.assert_called_with("run_cmd 'bash_cmd'", shell=True, check=True, cwd="repo_dir")
