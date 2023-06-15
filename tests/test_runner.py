from src.managers.runner import DockerManager


def test_docker_manager():
    docker = DockerManager("python:3.10-buster", "1.0.0", "test_dir")
    assert docker.image == "python:3.10-buster"
    assert docker.get_docker_image == "python:3.10-buster"
    assert (
        docker.run_cmd
        == f"docker run --name poetry-export -it --volume {docker.repo_dir}:/app -w /app {docker.image} bash -c"
    )
    assert (
        docker.run_args
        == "pip install -U pip && pip install poetry==1.0.0 && poetry export -f requirements.txt -o requirements-frozen.txt --without-hashes --dev"
    )
