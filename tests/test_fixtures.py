def test_rep_fixture(repo_fixture):
    assert repo_fixture.exists()
    assert (repo_fixture / "pyproject.toml").exists()
    assert (repo_fixture / "poetry.lock").exists()
    assert (repo_fixture / "Dockerfile").exists()


def test_package_fixture(package_fixture):
    info = package_fixture["info"]
    assert info["name"] == "wagtail-qrcode"
    assert info["version"] == "1.1.2"
    
    releases = package_fixture["releases"]
    assert isinstance(releases, dict)


def test_toml_fixture(toml_dev_fixture):
    assert toml_dev_fixture.is_file()


def test_toml_group_dev_fixture(toml_group_dev_fixture):
    assert toml_group_dev_fixture.is_file()


def test_frozen_fixture(frozen_fixture):
    assert frozen_fixture.is_file()
