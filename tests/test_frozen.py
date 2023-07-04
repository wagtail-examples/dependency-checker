import pytest
from src.parsers.frozen import FrozenParser


@pytest.fixture
def frozen_parser():
    return FrozenParser()


def test_parse_requirements(frozen_parser, tmp_path):
    # Create a temporary requirements-frozen.txt file with some example requirements
    requirements_file = tmp_path / "requirements-frozen.txt"
    requirements_file.write_text("requests==2.26.0\nnumpy==1.21.2\n")

    # Set the FrozenParser's file attribute to the temporary file
    frozen_parser.file = requirements_file

    # Call parse_requirements() to populate the requirements dictionary
    frozen_parser.parse_requirements()

    # Check that the requirements dictionary contains the expected packages and versions
    assert frozen_parser.requirements == {"requests": "2.26.0", "numpy": "1.21.2"}


def test_match_equals():
    # Test that match_equals() correctly extracts the package name and version from a line with ==
    frozen_parser = FrozenParser()
    package_name, package_version = frozen_parser.match_equals("requests==2.26.0")
    assert package_name == "requests"
    assert package_version == "2.26.0"


def test_match_repo():
    # Test that match_repo() correctly extracts the package name and repo URL from a line with @
    frozen_parser = FrozenParser()
    package_name, repo_url = frozen_parser.match_repo("requests@git+https://github.com/psf/requests.git")
    assert package_name == "requests"
    assert repo_url == "git+https://github.com/psf/requests.git"


def test_clean_up(frozen_parser, tmp_path):
    # Create a temporary requirements-frozen.txt file
    requirements_file = tmp_path / "requirements-frozen.txt"
    requirements_file.write_text("requests==2.26.0\nnumpy==1.21.2\n")

    # Set the FrozenParser's file attribute to the temporary file
    frozen_parser.file = requirements_file

    # Call clean_up() to delete the temporary file
    frozen_parser.clean_up()

    # Check that the temporary file no longer exists
    assert not requirements_file.exists()
