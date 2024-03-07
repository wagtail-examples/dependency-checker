# def test_dependencies(parsed_toml_dev):
#     # Check that the dependencies() method returns the expected dictionary
#     assert parsed_toml_dev.dependencies() == {"requests": "^2.26.0", "numpy": "^1.21.2"}


# def test_dev_dependencies(parsed_toml_group_dev):
#     # Check that the dev_dependencies() method returns the expected dictionary
#     assert parsed_toml_group_dev.dev_dependencies() == {"pytest": "^6.2.4"}


# def test_all_dependencies(parsed_toml_dev):
#     # Check that the all_dependencies() method returns the expected dictionary
#     assert parsed_toml_dev.all_dependencies() == {"requests": "^2.26.0", "numpy": "^1.21.2", "pytest": "^6.2.4"}


# def test_get_dependency_version(parsed_toml_dev):
#     # Check that the get_dependency_version() method returns the expected version string
#     assert parsed_toml_dev.get_dependency_version("requests") == "^2.26.0"
#     assert parsed_toml_dev.get_dependency_version("numpy") == "^1.21.2"
#     assert parsed_toml_dev.get_dependency_version("pytest") == "^6.2.4"


# def test_no_dependencies(parsed_toml_no_dependencies):
#     # Check that the dependencies() method returns an empty dictionary
#     assert True if not parsed_toml_no_dependencies.dependencies() else False
