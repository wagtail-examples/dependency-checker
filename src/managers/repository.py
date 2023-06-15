from os import name, path
import pathlib
import subprocess
import tempfile
import re

class RepositoryManager:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.temp_dir = tempfile.TemporaryDirectory(
            # cloning to the root of the project so we can access the files
            # for a short time it need be.
            dir=pathlib.Path(__file__).parent.parent.parent,
            prefix="docker-run-",
        )
        self.repo_dir = None

    def clone(self):
        self.repo_dir = pathlib.Path(self.temp_dir.name)
        try:
            subprocess.run(['git', 'clone', self.repo_url, self.temp_dir.name], check=True, capture_output=True)
            subprocess.run(["git", "status"], cwd=self.repo_dir, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            exit(f"Error cloning repository {self.repo_url}: {e}")

    def branch(self, branch_name):
        try:
            subprocess.run(["cd", self.repo_dir], check=True, capture_output=True)
            subprocess.run(['git', 'checkout', branch_name], cwd=self.repo_dir, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            exit(f"Error checking out branch {branch_name}: {e}")

    def toml_exists(self):
        return (self.repo_dir / "pyproject.toml").exists()
    
    # TODO: implement this
    # def requirements_exists(self):
    #     return (self.repo_dir / "requirements.txt").exists()
    
    def dockerfile_exists(self):
        return (self.repo_dir / "Dockerfile").exists()
    
    def remove_temp_dir(self):
        self.temp_dir.cleanup()

    @property
    def toml(self):
        return pathlib.Path(self.repo_dir / "pyproject.toml")
    
    # TODO: implement this
    # @property
    # def get_requirements(self):
    #     with open(self.repo_dir / "requirements.txt") as f:
    #         return f.read()
    
    @property
    def get_dockerfile(self):
        with open(self.repo_dir / "Dockerfile") as f:
            return f.read()
        
    @property
    def docker_image(self):
        return self.get_docker_image()
    
    @property
    def poetry_version(self):
        return self.get_poetry_version()

    
    def get_docker_image(self):
        content = self.get_dockerfile.split("\n")

        # parse this with a regex e.g. 'FROM python:3.9-buster as production'
        pattern = r"^FROM python:(.*?)"
        # result would be python:3.9-buster

        for line in content:
            if line.startswith("#"):
                continue # ignore comments
            match = re.search(pattern, line)
            if match:
                image = line.split(" ")[1].strip()
                return image
      
    def get_poetry_version(self):
        content = self.get_dockerfile.split("\n")
        
        # parse this with a regex e.g. ARG POETRY_VERSION=1.4.2
        pattern = r"^ARG POETRY_VERSION=(.*?)"
        # result would be ARG POETRY_VERSION=1.4.2

        for line in content:
            if line.startswith("#"):
                continue
            match = re.search(pattern, line)
            if match:
                poetry_version = line.split("=")[1].strip()
                return poetry_version
