from src.managers.package import Package


def test_package_instance():
    json = {
        "info": {"name": "requests", "version": "2.26.0"},
        "releases": {
            "2.25.1": [{"upload_time": "2021-10-01T00:00:00"}],
            "2.26.0": [
                {"upload_time": "2021-10-02T00:00:00"},
                {"upload_time": "2021-10-03T00:00:00"},
            ],
        },
    }
    package = Package(json)

    assert package.name == "requests"
    assert package.version == "2.26.0"
    assert package.releases == {
        "2.25.1": [{"upload_time": "2021-10-01T00:00:00"}],
        "2.26.0": [
            {"upload_time": "2021-10-02T00:00:00"},
            {"upload_time": "2021-10-03T00:00:00"},
        ],
    }

    assert package.current_version == "2.26.0"

    assert package.latest_version == "2.26.0"


def test_parse_versions_for_latest_with_pre_release():
    json = {
        "info": {"name": "requests", "version": "2.26.0"},
        "releases": {
            "2.25.1": [{"upload_time": "2021-10-01T00:00:00"}],
            "2.26.0": [
                {"upload_time": "2021-10-02T00:00:00"},
                {"upload_time": "2021-10-03T00:00:00"},
            ],
            "2.26.0rc1": [
                {"upload_time": "2021-10-04T00:00:00"},
                {"upload_time": "2021-10-05T00:00:00"},
            ],
        },
    }
    package = Package(json)

    latest_version = package.latest_version

    assert latest_version == "2.26.0"


def test_unknown_release_identifier():
    json = {
        "info": {"name": "requests", "version": "2.26.0"},
        "releases": {
            "2.25.1-bully": [{"upload_time": "2021-10-01T00:00:00"}],
        },
    }

    package = Package(json)
    package.latest_version
