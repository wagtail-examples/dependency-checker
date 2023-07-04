import pathlib
from dataclasses import dataclass

@dataclass
class FrozenParser:
    requirements = dict()

    def __post_init__(self) -> None:
        self.file = pathlib.Path(__file__).parent.parent.parent / "requirements-frozen.txt"


    def parse_requirements(self) -> None:
        if not self.file.is_file():
            return
    
        with open(self.file, "r") as f:
            match = None
            lines = f.readlines()
            for line in lines:
                if "@" in line:
                    match = self.match_repo(line)
                elif "==" in line:
                    match = self.match_equals(line)
                if match:
                    self.requirements[match[0]] = match[1]

    def match_equals(self, package_name):
        parts = package_name.split("==")
        if len(parts) == 2:
            package_name = parts[0].strip()
            package_version = parts[1].split(";")[0].strip()
            return package_name, package_version
        
    def match_repo(self, line):
        parts = line.split("@", 1)
        if len(parts) == 2:
            package_name = parts[0].strip()
            repo_url = parts[1].split(";")[0].strip()
            return package_name, repo_url

    def clean_up(self):
        self.file.unlink()
