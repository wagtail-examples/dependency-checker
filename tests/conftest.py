import os
import pathlib
import subprocess

import pytest

base_dir = pathlib.Path(__file__).resolve().parent.parent


@pytest.fixture
def typical_dockerfile_content():
    """Return the content of a typical Dockerfile for testing"""

    with open(base_dir / "tests/test_files/Dockerfile", "r") as f:
        return f.read()
    

@pytest.fixture
def unexpected_dockerfile_content():
    """Return the content of a typical Dockerfile for testing"""

    with open(base_dir / "tests/test_files/DockerfileNoPoetry", "r") as f:
        return f.read()


@pytest.fixture
def dockerfile_fixture(typical_dockerfile_content, tmp_path):
    """Create a dockerfile with content for testing"""

    dockerfile = tmp_path / "Dockerfile"
    lines = typical_dockerfile_content.split("\n")
    dockerfile.write_text("\n".join(lines))

    return dockerfile


@pytest.fixture
def dockerfile_fixture_no_poetry(unexpected_dockerfile_content, tmp_path):
    """Create a dockerfile with content for testing"""

    dockerfile = tmp_path / "Dockerfile"
    lines = unexpected_dockerfile_content.split("\n")
    dockerfile.write_text("\n".join(lines))

    return dockerfile


@pytest.fixture
def poetry_lock_content():
    """Return the content of a typical poetry.lock for testing"""

    with open(base_dir / "tests/test_files/poetry.lock", "r") as f:
        return f.read()


@pytest.fixture
def pyproject_content():
    """Return the content of a typical pyproject.toml for testing"""

    with open(base_dir / "tests/test_files/pyproject.toml", "r") as f:
        return f.read()


@pytest.fixture
def pyproject_fixture(pyproject_content, poetry_lock_content, tmp_path):
    """Create a pyproject.toml with content for testing"""

    pyproject = tmp_path / "pyproject.toml"
    lines = pyproject_content.split("\n")
    pyproject.write_text("\n".join(lines))

    poetry_lock = tmp_path / "poetry.lock"
    lines = poetry_lock_content.split("\n")
    poetry_lock.write_text("\n".join(lines))

    return pathlib.Path(pyproject).absolute()


@pytest.fixture
def not_modern_pyproject_content():
    """Return the content of a typical pyproject.toml for testing
    and modify it to use the old dev-dependencies key"""

    with open(base_dir / "tests/test_files/pyproject_not_modern.toml", "r") as f:
        return f.read()


@pytest.fixture
def pyproject_not_modern_fixture(not_modern_pyproject_content, poetry_lock_content, tmp_path):
    """Create a pyproject.toml with content for testing"""

    pyproject = tmp_path / "pyproject.toml"
    lines = not_modern_pyproject_content.split("\n")
    pyproject.write_text("\n".join(lines))

    poetry_lock = tmp_path / "poetry.lock"
    lines = poetry_lock_content.split("\n")
    poetry_lock.write_text("\n".join(lines))

    return pathlib.Path(pyproject).absolute()


@pytest.fixture
def requirements_content():
    """Return the content of a typical requirements.txt for testing"""

    with open(base_dir / "tests/test_files/requirements.txt", "r") as f:
        return f.read()


@pytest.fixture
def requirements_fixture(requirements_content, tmp_path):
    """Create a requirements.txt file with content for testing"""

    requirements_file = tmp_path / "requirements.txt"
    lines = requirements_content.split("\n")
    requirements_file.write_text("\n".join(lines))

    return pathlib.Path(requirements_file).absolute()


@pytest.fixture
def repo_content(pyproject_content, typical_dockerfile_content, poetry_lock_content, tmp_path):
    os.chdir(tmp_path)

    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "config", "--local", "user.name", "a"], check=True, capture_output=True)
    subprocess.run(["git", "config", "--local", "user.email", "a@b.com"], check=True, capture_output=True)
    subprocess.run(["git", "branch", "-M", "main"], check=True, capture_output=True)
    subprocess.run(["touch", "pyproject.toml"], check=True, capture_output=True)
    subprocess.run(["touch", "poetry.lock"], check=True, capture_output=True)
    subprocess.run(["touch", "Dockerfile"], check=True, capture_output=True)

    with open("pyproject.toml", "w") as f:
        f.write(pyproject_content)

    with open("poetry.lock", "w") as f:
        f.write(poetry_lock_content)

    with open("Dockerfile", "w") as f:
        f.write(typical_dockerfile_content)

    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add files"], check=True, capture_output=True)

    subprocess.run(["git", "branch", "test"], check=True, capture_output=True)

    return pathlib.Path(tmp_path).absolute()
