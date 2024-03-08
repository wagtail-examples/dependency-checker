from dataclasses import dataclass


@dataclass
class TextParser:
    """Parses a requirements.txt file to extract dependencies"""

    text_file: str
    dependencies: dict = None
    text_file_contents: str = None

    def __post_init__(self):
        self.text_file_contents = self._get_text_file_contents()
        self.dependencies = self._get_dependencies()

    def _get_text_file_contents(self):
        try:
            with open(self.text_file, "r") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _get_dependencies(self):
        contents = self.text_file_contents
        dependencies = {}

        for line in contents.split("\n"):
            if line and line.startswith("#"):
                continue

            if "==" in line:
                match = self.match_equals(line)
                dependencies[match[0]] = match[1]
                continue

            if "@" in line:
                match = self.match_repo(line)
                dependencies[match[0]] = match[1]
                continue

        return dependencies

    def match_equals(self, package_name):
        parts = package_name.split("==")
        package_name = parts[0].strip().lower()
        package_version = parts[1].split(";")[0].strip()
        return package_name, package_version

    def match_repo(self, line):
        parts = line.split("@", 1)
        package_name = parts[0].strip().lower()
        repo_url = parts[1].split(";")[0].strip()
        return package_name, repo_url
