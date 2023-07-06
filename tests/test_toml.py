import pytest
from src.parsers.toml import TomlParser


@pytest.fixture
def toml_parser(tmp_path):
    # Create a temporary pyproject.toml file with some example dependencies
    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(
        "[tool.poetry]\n"
        'name = "example"\n'
        'version = "0.1.0"\n'
        "[tool.poetry.dependencies]\n"
        'requests = "^2.26.0"\n'
        'numpy = "^1.21.2"\n'
        "[tool.poetry.dev-dependencies]\n"
        'pytest = "^6.2.4"\n'
    )

    # Create a TomlParser instance with the temporary file
    return TomlParser(file=pyproject_file)


def test_dependencies(toml_parser):
    # Check that the dependencies() method returns the expected dictionary
    assert toml_parser.dependencies() == {"requests": "^2.26.0", "numpy": "^1.21.2"}


def test_dev_dependencies(toml_parser):
    # Check that the dev_dependencies() method returns the expected dictionary
    assert toml_parser.dev_dependencies() == {"pytest": "^6.2.4"}


def test_all_dependencies(toml_parser):
    # Check that the all_dependencies() method returns the expected dictionary
    assert toml_parser.all_dependencies() == {"requests": "^2.26.0", "numpy": "^1.21.2", "pytest": "^6.2.4"}


def test_get_dependency_version(toml_parser):
    # Check that the get_dependency_version() method returns the expected version string
    assert toml_parser.get_dependency_version("requests") == "^2.26.0"
    assert toml_parser.get_dependency_version("numpy") == "^1.21.2"
    assert toml_parser.get_dependency_version("pytest") == "^6.2.4"
