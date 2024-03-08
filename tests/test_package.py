from src.managers.package import Package


# Package tests
def test_parse_versions_for_latest():
    # Testing for normal releases
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

    latest_version = package.latest_version

    assert latest_version == "2.26.0"


# def test_parse_versions_for_latest_with_release_candidate():
#     # Testing for release candidates that are later than the latest normal release
#     # because sometimes we use release candidates as normal releases
#     json = {
#         "info": {"name": "requests", "version": "2.26.0"},
#         "releases": {
#             "2.25.1": [{"upload_time": "2021-10-01T00:00:00"}],
#             "2.26.0rc1": [
#                 {"upload_time": "2021-10-02T00:00:00"},
#                 {"upload_time": "2021-10-03T00:00:00"},
#             ],
#             "2.26.0rc2": [
#                 {"upload_time": "2021-10-04T00:00:00"},
#                 {"upload_time": "2021-10-05T00:00:00"},
#             ],
#         },
#     }
#     package = Package(json)

#     latest_version = package.latest_version

#     assert latest_version == "2.26.0rc2"


def test_current_version():
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

    current_version = package.current_version

    assert current_version == "2.26.0"


def test_str():
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

    string = str(package)

    assert string == "requests 2.26.0"
