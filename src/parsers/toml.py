import pathlib
from dataclasses import dataclass

import tomli


@dataclass
class TomlParser:
    file: pathlib.Path

    def __post_init__(self):
        with open(self.file, "rb") as f:
            self.data = tomli.load(f)

    def dependencies(self):
        return self.data["tool"]["poetry"]["dependencies"]

    def dev_dependencies(self):
        if "dev-dependencies" in self.data["tool"]["poetry"]:
            return self.data["tool"]["poetry"]["dev-dependencies"]
        elif "group" in self.data["tool"]["poetry"]:
            return self.data["tool"]["poetry"]["group"]["dev"]["dependencies"]
        else:
            return {}

    def all_dependencies(self):
        return {**self.dependencies(), **self.dev_dependencies()}

    def get_dependency_version(self, dependency):
        return self.all_dependencies()[dependency]
