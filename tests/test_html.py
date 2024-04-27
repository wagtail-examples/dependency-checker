from src.reporters.html import HTMLReporter


def test_html_reporter_instance():
    reporter = HTMLReporter()
    assert isinstance(reporter, HTMLReporter)
    assert reporter.report_header.startswith("<!DOCTYPE html>")
    assert reporter.report_footer.startswith("</div>")
    assert reporter.report_info_section == ""
    assert reporter.report_production_section == ""
    assert reporter.report_development_section == ""
    assert reporter.info_data == {}
    assert reporter.production_data == []
    assert reporter.development_data == []
    assert reporter.report == ""


def test_add_info_data():
    reporter = HTMLReporter()
    reporter.add_info_data({"key": "value"})
    assert reporter.info_data == {"key": "value"}


def test_add_production_data():
    reporter = HTMLReporter()
    reporter.add_production_data({"key": "value"})
    assert reporter.production_data == [{"key": "value"}]


def test_add_development_data():
    reporter = HTMLReporter()
    reporter.add_development_data({"key": "value"})
    assert reporter.development_data == [{"key": "value"}]


def test_heading():
    reporter = HTMLReporter()
    assert reporter._heading("Heading") == "<h2>Heading</h2>\n"


def test_open_table():
    reporter = HTMLReporter()
    assert reporter._open_table("striped") == "<table class='striped'>\n"
    assert reporter._open_table("") == "<table class='striped'>\n"


def test_close_table():
    reporter = HTMLReporter()
    assert reporter._close_table() == "</table>\n"


def test_table_header():
    reporter = HTMLReporter()
    assert reporter._table_header(["Header1", "Header2"]) == "<thead><tr><th>Header1</th><th>Header2</th></tr></thead>"


def test_table_dependency_row():
    reporter = HTMLReporter()
    status_class = "status"
    data = {
        "Package": "Package",
        "Installed Version": "Installed Version",
        "Latest Version": "Latest Version",
        "Status": "Status",
    }
    assert (
        reporter._table_dependency_row(data, status_class)
        == """
            <tr>
                <td><span class='status'>Package</span></td>
                <td>Installed Version</td>
                <td>Latest Version</td>
                <td><span class='status'>Status</span></td>
            </tr>"""
    )


def test_gather_status_class():
    data = {
        "Package": "Package",
        "Installed Version": "Installed Version",
        "Latest Version": "Latest Version",
        "Status": "Not set",
    }

    reporter = HTMLReporter()
    assert reporter._gather_status_class(data) == "pico-color-red-500"

    data = {
        "Package": "Package",
        "Installed Version": "Installed Version",
        "Latest Version": "Latest Version",
        "Status": "Check",
    }

    reporter = HTMLReporter()
    assert reporter._gather_status_class(data) == "pico-color-cyan-500"

    data = {
        "Package": "Package",
        "Installed Version": "Installed Version",
        "Latest Version": "Latest Version",
        "Status": "Outdated",
    }

    reporter = HTMLReporter()
    assert reporter._gather_status_class(data) == "pico-color-orange-500"

    data = {
        "Package": "Package",
        "Installed Version": "Installed Version",
        "Latest Version": "Latest Version",
        "Status": "OK",
    }

    reporter = HTMLReporter()
    assert reporter._gather_status_class(data) == "pico-color-green-500"


def test_write_report():
    reporter = HTMLReporter()
    info_data = {
        "key": "value",
    }
    reporter.add_info_data(info_data)
    production_data = {
        "Package": "Package",
        "Installed Version": "Installed Version",
        "Latest Version": "Latest Version",
        "Status": "OK",
    }

    reporter.add_production_data(production_data)
    development_data = {
        "Package": "Package",
        "Installed Version": "Installed Version",
        "Latest Version": "Latest Version",
        "Status": "OK",
    }

    reporter.add_development_data(development_data)
    reporter.write_report()

    with open("report.html") as f:
        report = f.read()
        assert report.startswith("<!DOCTYPE html>")
