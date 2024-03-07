import subprocess
from dataclasses import dataclass, field


@dataclass
class DockerManager:
    image: str
    poetry_version: str
    repo_dir: str
    docker_run_name: str = field(default="poetry-export")
    run_command: str = field(init=False)

    def run_cmd(self):
        cmd = [
            "docker run --name",
            f"{self.docker_run_name}",
            "-it --rm --volume",
            f"{self.repo_dir}:/app",
            "-w /app",
            self.image,
            "bash -c",
        ]
        self.run_command = " ".join(cmd)
        return self.run_command

    def bash_cmd(self):
        cmd = [
            "pip install -U pip",
            f"pip install poetry=={self.poetry_version}",
            "poetry export -f requirements.txt -o requirements-frozen.txt --without-hashes --dev",
        ]
        self.bash_cmd = " && ".join(cmd)
        return self.bash_cmd

    def run(self, cmd, args):
        subprocess.run(f"{cmd} '{args}'", shell=True, check=True, cwd=self.repo_dir)
