import pathlib
import re
from dataclasses import dataclass


@dataclass
class DockerFileParser:
    """Parses a dockerfile to extract:
    - The base python image
    - The poetry version
    """

    dockerfile_path: pathlib.Path
    docker_image: str = None
    poetry_version: str = None

    def __post_init__(self):
        self.docker_image = self.get_docker_image()
        self.poetry_version = self.get_poetry_version()

    def _get_dockerfile(self):
        try:
            with open(self.dockerfile_path) as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def get_docker_image(self):
        content = self._get_dockerfile().split("\n")

        # parse this with a regex e.g. 'FROM python:3.9-buster as production'
        pattern = r"^FROM python:(.*?)"
        # result would be python:3.9-buster

        for line in content:
            if line.startswith("#"):
                continue  # ignore comments
            match = re.search(pattern, line)
            if match:
                image = line.split(" ")[1].strip()
                return image

    def get_poetry_version(self):
        content = self._get_dockerfile().split("\n")

        # parse this with a regex e.g. ARG POETRY_VERSION=1.4.2
        pattern = r"^ARG POETRY_VERSION=(.*?)"
        # result would be ARG POETRY_VERSION=1.4.2

        poetry_version = None

        for line in content:
            if line.startswith("#"):
                continue
            match = re.search(pattern, line)
            if match:
                poetry_version = line.split("=")[1].strip()

        return poetry_version
