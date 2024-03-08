from dataclasses import dataclass

import tomli


@dataclass
class TomlParser:
    """Parses a pyproject.toml file to extract:
    - Poetry dependencies
    - Poetry dev dependencies
    """

    pyproject_file_path: str
    dependencies: dict = None
    dev_dependencies: dict = None
    modern_poetry: bool = False
    pyproject_contents: dict = None

    def __post_init__(self):
        self.pyproject_contents = self._get_pyproject_contents()

        if self.pyproject_contents:
            if self._has_tool_poetry_group_dev_dependencies:
                self.modern_poetry = True

            self.dependencies = self.get_poetry_dependencies()
            self.dev_dependencies = self.get_poetry_dev_dependencies(self.modern_poetry)

    def _get_pyproject_contents(self):
        try:
            with open(self.pyproject_file_path, "rb") as f:
                return tomli.load(f)
        except FileNotFoundError:
            return {}

    @property
    def _has_tool_poetry_group_dev_dependencies(self):
        contents = self.pyproject_contents
        try:
            contents["tool"]["poetry"]["group"]["dev"]["dependencies"]
            return True
        except KeyError:
            return False

    def get_poetry_dependencies(self):
        contents = self.pyproject_contents
        return contents["tool"]["poetry"]["dependencies"]

    def get_poetry_dev_dependencies(self, modern_poetry: bool):
        contents = self.pyproject_contents
        if modern_poetry:
            return contents["tool"]["poetry"]["group"]["dev"]["dependencies"]
        else:
            return contents["tool"]["poetry"]["dev-dependencies"]
