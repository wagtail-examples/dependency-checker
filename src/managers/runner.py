import subprocess
import shutil

class DockerManager:
    def __init__(self, image, poetry_version=None, repo_dir=None):
        self.image = image
        self.poetry_version = poetry_version
        self.repo_dir = repo_dir

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
            "poetry-export",
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
            f"poetry export -f requirements.txt -o requirements-frozen.txt --without-hashes --dev",
        ]

        return " && ".join(args)
    

    def run(self, cmd, args):
        """Run the dockerfile and extract the installed dependencies"""
        # run the args in the docker container
        try:
            # remove the docker container if it exists, sometimes it gets left behind after an error
            subprocess.run(["docker", "rm", "poetry-export"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            pass
        subprocess.run(f"{cmd} '{args}'", shell=True, check=True, capture_output=True)
        shutil.copy(
            # requirements-frozen.txt will be copied to the local filesystem
            self.repo_dir / "requirements-frozen.txt",
            "requirements-frozen.txt",
        )
        subprocess.run(["docker", "stop", "poetry-export"], check=True, capture_output=True)
