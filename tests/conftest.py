import pytest
import pathlib
import shutil
import subprocess
from tempfile import TemporaryDirectory
import json


@pytest.fixture
def repo_fixture():
    fixtures = pathlib.Path(__file__).parent / "fixtures" / "test_repo"
    temp_dir = pathlib.Path(TemporaryDirectory().name)

    # Copy the contents of the fixtures folder to the temporary directory
    shutil.copytree(fixtures, temp_dir)

    # Initialize the temporary directory as a Git repository
    subprocess.run(["git", "init"], cwd=temp_dir, check=True)

    # Change the default branch name to "main"
    # subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], cwd=temp_dir, check=True)
    subprocess.run(["git", "branch", "-m", "master", "main"], cwd=temp_dir, check=True)

    # Add the files and commit
    subprocess.run(["git", "add", "."], cwd=temp_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=temp_dir, check=True)

    # show the git status
    subprocess.run(["git", "status"], cwd=temp_dir, check=True)

    # create a branch
    subprocess.run(["git", "checkout", "-b", "test-branch"], cwd=temp_dir, check=True)

    # switch back to main
    subprocess.run(["git", "checkout", "main"], cwd=temp_dir, check=True)

    # Return the path to the temporary directory
    yield temp_dir

    # Remove the temporary directory after the test has finished
    # shutil.rmtree(temp_dir)


@pytest.fixture
def package_fixture():
    fixtures = pathlib.Path(__file__).parent / "fixtures" / "responses"
    file = open(fixtures / "package.json", "rb").read()
    package = json.loads(file)
    return package


@pytest.fixture
def toml_dev_fixture():
    return pathlib.Path(__file__).parent / "fixtures" / "toml" / "pyproject_dev_deps.toml"
    # fixtures = pathlib.Path(__file__).parent / "fixtures" / "toml"
    # file = open(fixtures / "pyproject_dev_deps.toml", "rb")
    # return file


@pytest.fixture
def toml_group_dev_fixture():
    return pathlib.Path(__file__).parent / "fixtures" / "toml" / "pyproject_group_dev_deps.toml"
    # fixtures = pathlib.Path(__file__).parent / "fixtures" / "toml"
    # file = open(fixtures / "pyproject_group_dev_deps.toml", "rb")
    # return file


@pytest.fixture
def frozen_fixture():
    fixtures = pathlib.Path(__file__).parent / "fixtures" / "files"
    return fixtures / "requirements-frozen.txt"
