from src.parsers.docker import DockerFileParser
from src.parsers.text import TextParser
from src.parsers.toml import TomlParser


def test_match_docker_python_image(dockerfile_fixture):
    """Test that the parser can match the base python image"""

    parser = DockerFileParser(dockerfile_fixture)

    assert parser.docker_image == "python:3.11-slim-bullseye"


def test_match_docker_poetry_version(dockerfile_fixture):
    """Test that the parser can match the poetry version"""

    parser = DockerFileParser(dockerfile_fixture)
    poetry_version = parser.get_poetry_version()

    assert poetry_version == "1.3.2"


def test_match_docker_poetry_not_found(dockerfile_fixture_no_poetry):
    """Test that the parser returns None if poetry is not found"""

    parser = DockerFileParser(dockerfile_fixture_no_poetry)
    poetry_version = parser.get_poetry_version()

    assert poetry_version is None


def test_docker_parser_file_error():
    """Test that the parser can handle a file not found error"""

    parser = DockerFileParser("non_existent_file.dockerfile")
    parser.dockerfile_contents = ""


def test_with_modern_dependencies(pyproject_fixture):
    """Test that the parser can match the poetry group dev dependencies"""

    parser = TomlParser(pyproject_fixture)

    assert parser.modern_poetry
    assert parser.dependencies["python"] == "^3.9"
    assert parser.dependencies["django"] == "~4.2"
    # more dependencies could be tested here
    assert parser.dependencies["wagtail"] == "~5.2"

    assert parser.dev_dependencies["black"] == "^24.2.0"
    assert parser.dev_dependencies["isort"] == "^5.13.2"
    # more dev dependencies could be tested here
    assert parser.dev_dependencies["flake8"] == "^7.0.0"


def test_with_not_modern_dependencies(pyproject_not_modern_fixture):
    """Test that the parser can match the poetry dev dependencies"""

    parser = TomlParser(pyproject_not_modern_fixture)

    assert not parser.modern_poetry
    assert parser.dependencies["python"] == "^3.9"
    assert parser.dependencies["django"] == "~4.2"
    # more dependencies could be tested here
    assert parser.dependencies["wagtail"] == "~5.2"

    assert parser.dev_dependencies["black"] == "^24.2.0"
    assert parser.dev_dependencies["isort"] == "^5.13.2"
    # more dev dependencies could be tested here
    assert parser.dev_dependencies["flake8"] == "^7.0.0"


def test_toml_parser_file_error():
    """Test that the parser can handle a file not found error"""

    parser = TomlParser("non_existent_file.toml")
    parser.pyproject_contents = {}


def test_requirements_file_error():
    """Test that the parser can handle a file not found error"""

    parser = TextParser("non_existent_file.requirements")

    assert parser.text_file_contents == ""


def test_requirements(requirements_fixture):
    """Test that the parser can match in the requirements file"""

    parser = TextParser(requirements_fixture)

    assert parser.dependencies["django"] == "4.2.11"
    assert parser.dependencies["wagtail"] == "5.2.3"
    # more dependencies could be tested here
    assert parser.dependencies["black"] == "24.2.0"
