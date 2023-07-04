from dataclasses import dataclass
import requests
import datetime


class Client:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get(self, package_name):
        response = self.session.get(f"{self.url}/{package_name}/json")
        if response.status_code == 200:
            # known package
            return response
        else:
            # unknown package
            return response.status_code



@dataclass
class Package:
    json: dict

    def __post_init__(self):
        self.name = self.json["info"]["name"]
        self.version = self.json["info"]["version"]
        self.releases = self.json["releases"]
    
    @property
    def current_version(self):
        return self.version
    
    @property
    def latest_version(self):
        return self.parse_versions_for_latest()
    
    def parse_versions_for_latest(self):
        # find the release with the latest upload_time
        latest_date = None
        latest_version = None
        for version, releases in self.releases.items():
            for release in releases:
                upload_time = datetime.datetime.fromisoformat(release["upload_time"])
                if latest_date is None or upload_time > latest_date:
                    latest_date = upload_time
                    latest_version = version
        return latest_version
    
    def __str__(self):
        return f"{self.name} {self.version}"

