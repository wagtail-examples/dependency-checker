import os
import pathlib
import subprocess

import pytest

# from src.managers.repository import RepositoryManager
# from src.parsers.toml import TomlParser


@pytest.fixture
def typical_dockerfile_content():
    """Return the content of a typical Dockerfile for testing"""

    with open("tests/file_fixtures/docker.txt", "r") as f:
        return f.read()


@pytest.fixture
def dockerfile_fixture(typical_dockerfile_content, tmpdir):
    """Create a dockerfile with content for testing"""

    dockerfile = tmpdir.join("Dockerfile")
    lines = typical_dockerfile_content.split("\n")
    dockerfile.write("\n".join(lines))

    return pathlib.Path(dockerfile).absolute()


@pytest.fixture
def pyproject_content():
    """Return the content of a typical pyproject.toml for testing"""

    with open("tests/file_fixtures/pyproject.txt", "r") as f:
        return f.read()


@pytest.fixture
def pyproject_fixture(pyproject_content, tmpdir):
    """Create a pyproject.toml with content for testing"""

    pyproject = tmpdir.join("pyproject.toml")
    lines = pyproject_content.split("\n")
    pyproject.write("\n".join(lines))

    return pathlib.Path(pyproject).absolute()


@pytest.fixture
def not_modern_pyproject_content():
    """Return the content of a typical pyproject.toml for testing
    and modify it to use the old dev-dependencies key"""

    with open("tests/file_fixtures/pyproject_not_modern.txt", "r") as f:
        return f.read()


@pytest.fixture
def pyproject_not_modern_fixture(not_modern_pyproject_content, tmpdir):
    """Create a pyproject.toml with content for testing"""

    pyproject = tmpdir.join("pyproject.toml")
    lines = not_modern_pyproject_content.split("\n")
    pyproject.write("\n".join(lines))

    return pathlib.Path(pyproject).absolute()


@pytest.fixture
def requirements_content():
    """Return the content of a typical requirements.txt for testing"""

    with open("tests/file_fixtures/requirements.txt", "r") as f:
        return f.read()


@pytest.fixture
def requirements_fixture(requirements_content, tmpdir):
    """Create a requirements.txt file with content for testing"""

    requirements_file = tmpdir.join("requirements.txt")
    lines = requirements_content.split("\n")
    requirements_file.write("\n".join(lines))

    return requirements_file


@pytest.fixture()
def repo_content(tmpdir, pyproject_content, typical_dockerfile_content):
    os.chdir(tmpdir)

    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "branch", "-M", "main"], check=True, capture_output=True)
    subprocess.run(["touch", "pyproject.toml"], check=True, capture_output=True)
    subprocess.run(["touch", "Dockerfile"], check=True, capture_output=True)

    with open("pyproject.toml", "w") as f:
        f.write(pyproject_content)

    with open("Dockerfile", "w") as f:
        f.write(typical_dockerfile_content)

    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add files"], check=True, capture_output=True)

    subprocess.run(["git", "branch", "test"], check=True, capture_output=True)

    return pathlib.Path(tmpdir).absolute()


# @pytest.fixture
# def repository_manager(repo):
#     return RepositoryManager(repo_url=repo, docker_file_name="Dockerfile")


# @pytest.fixture
# def parsed_toml_dev(tmp_path):
#     # Create a temporary pyproject.toml file with some example dependencies
#     pyproject_file = tmp_path / "pyproject.toml"
#     pyproject_file.write_text(
#         "[tool.poetry]\n"
#         'name = "example"\n'
#         'version = "0.1.0"\n'
#         "[tool.poetry.dependencies]\n"
#         'requests = "^2.26.0"\n'
#         'numpy = "^1.21.2"\n'
#         "[tool.poetry.dev-dependencies]\n"
#         'pytest = "^6.2.4"\n'
#     )

#     # Create a TomlParser instance with the temporary file
#     return TomlParser(file=pyproject_file)


# @pytest.fixture
# def parsed_toml_group_dev(tmp_path):
#     # Create a temporary pyproject.toml file with some example dependencies
#     pyproject_file = tmp_path / "pyproject.toml"
#     pyproject_file.write_text(
#         "[tool.poetry]\n"
#         'name = "example"\n'
#         'version = "0.1.0"\n'
#         "[tool.poetry.dependencies]\n"
#         'requests = "^2.26.0"\n'
#         'numpy = "^1.21.2"\n'
#         "[tool.poetry.group.dev.dependencies]\n"
#         'pytest = "^6.2.4"\n'
#     )

#     # Create a TomlParser instance with the temporary file
#     return TomlParser(file=pyproject_file)


# @pytest.fixture
# def parsed_toml_no_dependencies(tmp_path):
#     # Create a temporary pyproject.toml file with no dependencies
#     pyproject_file = tmp_path / "pyproject.toml"
#     pyproject_file.write_text("[tool.poetry]\n" 'name = "example"\n' 'version = "0.1.0"\n')

#     # Create a TomlParser instance with the temporary file
#     return TomlParser(file=pyproject_file)
