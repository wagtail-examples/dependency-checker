import pathlib
from dataclasses import dataclass


@dataclass
class FrozenParser:
    requirements = dict()

    def __post_init__(self):
        self.file = pathlib.Path(__file__).parent.parent.parent / "requirements-frozen.txt" or None

    def parse_requirements(self):
        if self.file is None:
            return  # pragma: no cover
        if not self.file.is_file():
            return  # pragma: no cover

        with open(self.file, "r") as f:
            for line in f.readlines():
                if "==" in line:
                    match = self.match_equals(line)
                    self.requirements[match[0]] = match[1]
                    continue

                if "@" in line:
                    match = self.match_repo(line)
                    self.requirements[match[0]] = match[1]
                    continue

    def match_equals(self, package_name):
        parts = package_name.split("==")
        package_name = parts[0].strip()
        package_version = parts[1].split(";")[0].strip()
        return package_name, package_version

    def match_repo(self, line):
        parts = line.split("@", 1)
        package_name = parts[0].strip()
        repo_url = parts[1].split(";")[0].strip()
        return package_name, repo_url

    def clean_up_frozen(self):
        self.file.unlink()
