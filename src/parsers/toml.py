import pathlib
import tomli
from dataclasses import dataclass

@dataclass
class TomlParser:
    file: str
    data: dict = None

    def __post_init__(self):
        with open(self.file, "rb") as f:
            self.data = tomli.load(f)

    @property
    def dependencies(self):
        return self.data["tool"]["poetry"]["dependencies"]
    
    @property
    def dev_dependencies(self):
        if "dev-dependencies" in self.data["tool"]["poetry"]:
            return self.data["tool"]["poetry"]["dev-dependencies"]
        elif "group" in self.data["tool"]["poetry"]:
            return self.data["tool"]["poetry"]["group"]["dev"]["dependencies"]
    
    @property
    def all_dependencies(self):
        return {**self.dependencies, **self.dev_dependencies}
    
    def get_dependency_version(self, dependency):
        return self.all_dependencies[dependency]
