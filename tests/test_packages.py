from src.managers.package import Package

def test_package(package_fixture):
    package = Package(package_fixture)
    assert package.name == "wagtail-qrcode"
    assert package.version == "1.1.2"
    assert package.current_version == "1.1.2"
    assert package.latest_version == "1.1.2"

