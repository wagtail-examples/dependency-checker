import requests


class BaseClient(requests.Session):
    api_url = "https://pypi.org/pypi"

    def get_package(self):
        raise NotImplementedError


class PyPiClient(BaseClient):
    def __init__(self, url=None):
        super().__init__()
        self.url = self.api_url if not url else url

    def get_package(self, package_name=None):
        if package_name:
            response = self.get(f"{self.url}/{package_name}/json")
            if response.status_code == 200:
                # known package
                return response
            else:
                # unknown package
                return response.status_code
