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

    def __post_init__(self):
        self.repo_dir = tempfile.TemporaryDirectory(
            # cloning to the root of the project so we can access the files if needed
            dir=pathlib.Path(__file__).parent.parent.parent,
            prefix="docker-run-",
        )
        self._clone()

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

    def get_branches(self):
        branches = (
            subprocess.run(
                ["git", "branch", "--remote"],
                cwd=self.repo_dir.name,
                check=True,
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .strip()
            .split("\n")
        )
        branches_cleaned = []

        for branch in branches:
            branches_cleaned.append(branch.replace("origin/", "").strip())

        branch_index = {}
        for i, branch in enumerate(sorted(branches_cleaned), 1):
            branch_name = branch
            if branch == self.get_branch():
                branch_name = f"{branch} ( DEFAULT )"
            branch_index[i] = branch_name

        return branch_index

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
        pattern = r"^FROM.*?(python:?\d*\.*\d*\.*?).*"
        # result would be python:3.9

        python_image = None

        for line in content:

            if line.startswith("#"):
                continue

            match = re.search(pattern, line)

            if match:
                image = match.group(1)
                python_image = image
                break
        
        self.docker_image = python_image
        

    def parse_poetry_version(self):
        with open(self.dockerfile_path) as f:
            content = f.read().split("\n")

        # parse this with a regex e.g. ARG POETRY_VERSION=1.4.2
        pattern = r"^ARG.*?POETRY_VERSION=(.*)"
        # result would be 1.4.2

        poetry_version = None

        for line in content:

            if line.startswith("#"):
                continue

            match = re.search(pattern, line)

            if match:
                version = match.group(1)
                poetry_version = version

        self.poetry_version = poetry_version
