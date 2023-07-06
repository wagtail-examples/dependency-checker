import pytest
from src.managers.runner import DockerManager


@pytest.fixture
def docker_manager(tmpdir):
    return DockerManager(
        "python",
        "3.9.7",
        tmpdir,
    )


def test_docker_manager(docker_manager):
    assert docker_manager.get_docker_image == "python"
    assert docker_manager.run_cmd == (
        "docker run --name poetry-export -it --volume " f"{docker_manager.repo_dir}:/app -w /app python bash -c"
    )
    assert docker_manager.run_args == (
        "pip install -U pip && pip install poetry==3.9.7 && "
        "poetry export -f requirements.txt -o requirements-frozen.txt "
        "--without-hashes --dev"
    )
