import pathlib
import shutil
import subprocess


class DockerManager:
    def __init__(self, image, poetry_version=None, repo_dir=None, docker_run_name="poetry-export"):
        self.image = image
        self.poetry_version = poetry_version
        self.repo_dir = repo_dir
        self.base_dir = pathlib.Path(__file__).parent.parent.parent
        self.docker_run_name = docker_run_name
        # if the last run failed, the docker container may still exist
        self.cleanup_docker()

    @property
    def get_docker_image(self):
        """Return the docker image"""
        return self.image

    @property
    def run_cmd(self):
        """Return the docker run command"""
        cmd = [
            "docker",
            "run",
            "--name",
            f"{self.docker_run_name}",
            "-it",
            "--volume",
            f"{self.repo_dir}:/app",
            "-w",
            "/app",
            self.image,
            "bash -c",
        ]
        return " ".join(cmd)

    @property
    def run_args(self):
        """Return the docker run args"""
        args = [
            "pip install -U pip",
            f"pip install poetry=={self.poetry_version}",
            "poetry export -f requirements.txt -o requirements-frozen.txt --without-hashes --dev",
        ]

        return " && ".join(args)

    def run(self, cmd, args):
        """Run the dockerfile and extract the installed dependencies"""
        subprocess.run(f"{cmd} '{args}'", shell=True, check=True, capture_output=True)
        shutil.move(self.repo_dir / "requirements-frozen.txt", self.base_dir / "requirements-frozen.txt")
        subprocess.run(["docker", "stop", self.docker_run_name], check=True, capture_output=True)

    def cleanup_docker(self):
        try:
            # remove the docker container if it exists, sometimes it gets left behind after an error
            subprocess.run(["docker", "rm", self.docker_run_name], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            pass
