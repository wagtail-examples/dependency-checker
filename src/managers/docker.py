import subprocess
from dataclasses import dataclass, field


@dataclass
class DockerManager:
    image: str
    poetry_version: str
    repo_dir: str
    docker_run_name: str = field(default="poetry-export")
    run_cmd: str = field(init=False)
    bash_cmd: str = field(init=False)

    def __post_init__(self):
        self.generate_run_command()
        self.generate_bash_command()

    def generate_run_command(self):
        cmd = [
            "docker run --name",
            f"{self.docker_run_name}",
            "-it --rm --volume",
            f"{self.repo_dir}:/app",
            "-w /app",
            self.image,
            "bash -c",
        ]
        self.run_cmd = " ".join(cmd)

    def generate_bash_command(self):
        cmd = [
            "pip install -U pip",
            f"pip install poetry=={self.poetry_version}",
            "poetry export -f requirements.txt -o requirements-frozen.txt --without-hashes --dev",
        ]
        self.bash_cmd = " && ".join(cmd)

    def run(self, run_cmd=None, bash_cmd=None):
        if run_cmd and bash_cmd:
            subprocess.run(f"{run_cmd} '{bash_cmd}'", shell=True, check=True, cwd=self.repo_dir)
        else:
            subprocess.run(f"{self.run_cmd} '{self.bash_cmd}'", shell=True, check=True, cwd=self.repo_dir)
