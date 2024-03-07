import pathlib
import re
import subprocess
import tempfile
from dataclasses import dataclass, field


@dataclass
class RepositoryManager:
    repo_url: str
    repo_dir: tempfile.TemporaryDirectory = field(init=False)
    dockerfile_path: str = field(init=False)
    # dockerfile_name: str = field(init=False, default="Dockerfile")
    # docker_image: str = field(init=False)
    # poetry_version: str = field(init=False)

    def __post_init__(self):
        self.repo_dir = tempfile.TemporaryDirectory(
            # cloning to the root of the project so we can access the files if needed
            dir=pathlib.Path(__file__).parent.parent.parent,
            prefix="docker-run-",
        )
        self._clone()
        # self.docker_image = self.get_docker_image()
        # self.poetry_version = self.get_poetry_version()

    def _clone(self):
        subprocess.run(
            ["git", "clone", self.repo_url, self.repo_dir.name],
            check=True,
            capture_output=True,
        )

    @property
    def get_repo_dir(self):
        return pathlib.Path(self.repo_dir.name)

    def find_docker_files(self):
        return list(pathlib.Path(self.repo_dir.name).glob("**/Dockerfile*"))

    def get_branch(self):
        return (
            subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_dir.name,
                check=True,
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .strip()
        )

    def change_branch(self, branch_name):
        try:
            return (
                subprocess.run(
                    ["git", "checkout", branch_name],
                    cwd=self.repo_dir.name,
                    check=True,
                    capture_output=True,
                )
                .stdout.decode("utf-8")
                .strip()
            )
        except subprocess.CalledProcessError:
            return f"Error: Branch {branch_name} does not exist in the repository. Please check the branch name and try again."  # noqa

    def parse_docker_image(self):

        with open(self.dockerfile_path) as f:
            content = f.read().split("\n")

        # parse this with a regex e.g. 'FROM python:3.9-buster as production'
        pattern = r"^FROM python:(.*?)"
        # result would be python:3.9-buster

        for line in content:

            if line.startswith("#"):
                continue  # ignore comments

            match = re.search(pattern, line)

            if match:
                image = line.split(" ")[1].strip()
                self.docker_image = image

    def parse_poetry_version(self):
        with open(self.dockerfile_path) as f:
            content = f.read().split("\n")

        # parse this with a regex e.g. ARG POETRY_VERSION=1.4.2
        pattern = r"^ARG POETRY_VERSION=(.*?)"
        # result would be ARG POETRY_VERSION=1.4.2

        for line in content:

            if line.startswith("#"):
                continue

            match = re.search(pattern, line)

            if match:
                version = line.split("=")[1].strip()
                self.poetry_version = version


# class RepositoryManager:
#     def __init__(self, repo_url, docker_file_name):
#         self.repo_url = repo_url
#         self.temp_dir = tempfile.TemporaryDirectory(
#             # cloning to the root of the project so we can access the files
#             dir=pathlib.Path(__file__).parent.parent.parent,
#             prefix="docker-run-",
#         )
#         self.docker_file_name = docker_file_name

#     def clone(self):
#         self.repo_dir = pathlib.Path(self.temp_dir.name)
#         try:
#             console = Console()
#             console.print(f"Cloning repository {self.repo_url}...", style="yellow1")
#             subprocess.run(
#                 ["git", "clone", self.repo_url, self.temp_dir.name],
#                 check=True,
#                 capture_output=True,
#             )
#             subprocess.run(["git", "status"], cwd=self.repo_dir, check=True, capture_output=True)
#         except subprocess.CalledProcessError:
#             console = Console()
#             console.print(
#                 f"Error cloning repository {self.repo_url}: Please check the URL and try again.", style="red1"
#             )
#             exit()

#     def branch(self, branch_name):
#         try:
#             subprocess.run(["cd", self.repo_dir], check=True, capture_output=True)
#             subprocess.run(
#                 ["git", "checkout", branch_name],
#                 cwd=self.repo_dir,
#                 check=True,
#                 capture_output=True,
#             )
#         except subprocess.CalledProcessError:
#             console = Console()
#             console.print(
#                 f"Error checking out branch {branch_name}: Please check the branch name and try again.", style="red1"
#             )
#             exit()

#     def toml_exists(self):
#         return (self.repo_dir / "pyproject.toml").exists()

#     def dockerfile_exists(self):
#         return (self.repo_dir / self.docker_file_name).exists()

#     def remove_temp_dir(self):
#         self.temp_dir.cleanup()

#     @property
#     def toml(self):
#         return pathlib.Path(self.repo_dir / "pyproject.toml")

#     @property
#     def get_dockerfile(self):
#         try:
#             with open(self.repo_dir / self.docker_file_name) as f:
#                 return f.read()
#         except FileNotFoundError:
#             console = Console()
#             console.print(
#                 f"Error reading Dockerfile: {self.docker_file_name} not found in repository {self.repo_url}",
#                 style="red1",
#             )
#             exit()

#     @property
#     def docker_image(self):
#         try:
#             return self.get_docker_image()
#         except Exception as e:
#             exit(f"Error getting docker image: {e}")

#     @property
#     def poetry_version(self):
#         return self.get_poetry_version()

#     def get_docker_image(self):
#         content = self.get_dockerfile.split("\n")

#         # parse this with a regex e.g. 'FROM python:3.9-buster as production'
#         pattern = r"^FROM python:(.*?)"
#         # result would be python:3.9-buster

#         for line in content:
#             if line.startswith("#"):
#                 continue  # ignore comments
#             match = re.search(pattern, line)
#             if match:
#                 image = line.split(" ")[1].strip()
#                 return image

#     def get_poetry_version(self):
#         content = self.get_dockerfile.split("\n")

#         # parse this with a regex e.g. ARG POETRY_VERSION=1.4.2
#         pattern = r"^ARG POETRY_VERSION=(.*?)"
#         # result would be ARG POETRY_VERSION=1.4.2

#         for line in content:
#             if line.startswith("#"):
#                 continue
#             match = re.search(pattern, line)
#             if match:
#                 poetry_version = line.split("=")[1].strip()
#                 return poetry_version
