from src.parsers.toml import TomlParser
from src.parsers.frozen import FrozenParser


def test_toml_parser(toml_dev_fixture):
    toml = TomlParser(toml_dev_fixture)
    assert isinstance(toml.data, dict)
    assert isinstance(toml.dependencies, dict)
    assert "Django" in toml.dependencies
    assert isinstance(toml.dev_dependencies, dict)
    assert "black" in toml.dev_dependencies
    assert isinstance(toml.all_dependencies, dict)
    assert "Django" in toml.all_dependencies
    assert "black" in toml.all_dependencies
    assert toml.get_dependency_version("Django") == "3.2.14"


def test_toml_group_dev_parser(toml_group_dev_fixture):
    toml = TomlParser(toml_group_dev_fixture)
    assert isinstance(toml.data, dict)
    assert isinstance(toml.dependencies, dict)
    assert "Django" in toml.dependencies
    assert isinstance(toml.dev_dependencies, dict)
    assert "black" in toml.dev_dependencies
    assert isinstance(toml.all_dependencies, dict)
    assert "Django" in toml.all_dependencies
    assert "black" in toml.all_dependencies
    assert toml.get_dependency_version("Django") == "3.2.14"


def test_frozen_parser(frozen_fixture):
    frozen_parser = FrozenParser(frozen_fixture)
    assert frozen_parser.file.is_file()
    assert isinstance(frozen_parser.requirements, dict)

    frozen_parser.parse_requirements()
    assert isinstance(frozen_parser.requirements, dict)
    assert "django" in frozen_parser.requirements
    assert "wagtail-sharing" in frozen_parser.requirements
    assert frozen_parser.requirements["django"] == "3.2.14"
    assert (
        frozen_parser.requirements["wagtail-sharing"]
        == "git+https://github.com/nickmoreton/wagtail-sharing@support/wagtail42-tokenurls"
    )


def test_frozen_parser_match_repo_line(frozen_fixture):
    frozen_parser = FrozenParser(frozen_fixture)
    repo_line = 'wagtail-sharing @ git+https://github.com/nickmoreton/wagtail-sharing@support/wagtail42-tokenurls ; python_version >= "3.8" and python_version < "4.0"'
    result = frozen_parser.match_repo(repo_line)
    assert result[0] == "wagtail-sharing"
    assert (
        result[1]
        == "git+https://github.com/nickmoreton/wagtail-sharing@support/wagtail42-tokenurls"
    )


def test_frozen_parser_match_equals_line(frozen_fixture):
    frozen_parser = FrozenParser(frozen_fixture)
    equals_line = "django==3.2.14"
    result = frozen_parser.match_equals(equals_line)
    assert result[0] == "django"
    assert result[1] == "3.2.14"
