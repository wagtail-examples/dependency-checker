import unittest
from unittest.mock import MagicMock

from src.client import PyPiClient


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


# if __name__ == '__main__':
#     unittest.main()


# import pytest

# from unittest.mock import Mock

# from src.client import BaseClient, PyPiClient as Client


# # Client tests
# def test_get_known_package():
#     # OK response
#     client = Client()
#     package_name = "requests"
#     expected_status_code = 200
#     expected_response = expected_status_code
#     session_mock = Mock()
#     session_mock.get.return_value = Mock(status_code=expected_status_code)
#     client.session = session_mock

#     response = client.get(package_name)

#     assert response == expected_response


# def test_get_unknown_package():
#     # Not Found response
#     url = "http://example.com"
#     package_name = "nonexistent_package"
#     expected_status_code = 404
#     expected_response = expected_status_code
#     session_mock = Mock()
#     session_mock.get.return_value = Mock(status_code=expected_status_code)
#     client = Client(url)
#     client.session = session_mock

#     response = client.get(package_name)

#     assert response == expected_response


# def test_client():
#     # Test client instance

#     class MyClient(BaseClient):
#         pass

#     client = MyClient()
#     assert client.api_url == "https://pypi.org/pypi"

#     with pytest.raises(NotImplementedError):
#         client.get_package()
