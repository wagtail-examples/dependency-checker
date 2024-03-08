import unittest
from unittest.mock import MagicMock

from src.client import BaseClient, PyPiClient


class TestPyPiClient(unittest.TestCase):
    def test_get_package_known_package(self):
        client = PyPiClient()
        package_name = "requests"  # assuming "requests" is a known package
        expected_status_code = 200
        mock_response = MagicMock(status_code=expected_status_code)

        with unittest.mock.patch("src.client.requests.Session.get") as mock_get:
            mock_get.return_value = mock_response
            response = client.get_package(package_name)

        self.assertEqual(response.status_code, expected_status_code)

    def test_get_package_unknown_package(self):
        client = PyPiClient()
        package_name = "nonexistent_package"  # assuming this package doesn't exist
        expected_status_code = 404
        mock_response = MagicMock(status_code=expected_status_code)

        with unittest.mock.patch("src.client.requests.Session.get") as mock_get:
            mock_get.return_value = mock_response
            response = client.get_package(package_name)

        self.assertEqual(response, expected_status_code)

    def test_not_implemented_error(self):
        class MyClient(BaseClient):
            pass

        with self.assertRaises(NotImplementedError):
            MyClient().get_package()
