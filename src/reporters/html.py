from dataclasses import dataclass


@dataclass
class HTMLReporter:
    report_header: str = ""
    report_footer: str = ""

    report_info_section: str = ""
    report_production_section: str = ""
    report_development_section: str = ""

    def __post_init__(self):
        with open("report_header.html") as f:
            self.report_header = f.read()

        with open("report_footer.html") as f:
            self.report_footer = f.read()

        self.info_data = {}
        self.production_data = []
        self.development_data = []

        self.report = ""

    def add_info_data(self, data: dict) -> None:
        self.info_data = data

    def add_production_data(self, data: dict) -> None:
        self.production_data.append(data)

    def add_development_data(self, data: dict) -> None:
        self.development_data.append(data)

    def _heading(self, heading: str) -> str:
        return f"<h2>{heading}</h2>\n"

    def _open_table(self, cls: str) -> str:
        if not cls:
            cls = "striped"
        return f"<table class='{cls}'>\n"

    def _close_table(self) -> str:
        return "</table>\n"

    def _table_header(self, headers: list) -> str:
        header = "<thead><tr>"
        for h in headers:
            header += f"<th>{h}</th>"
        header += "</tr></thead>"
        return header

    def _table_dependency_row(self, data: dict, status_class: str) -> str:
        return f"""
            <tr>
                <td><span class='{status_class}'>{data['Package']}</span></td>
                <td>{data['Installed Version']}</td>
                <td>{data['Latest Version']}</td>
                <td><span class='{status_class}'>{data['Status']}</span></td>
            </tr>"""

    def _gather_status_class(self, data: list) -> str:
        status_class = "pico-color-red-500"
        if data["Status"] == "Check":
            status_class = "pico-color-cyan-500"
        elif data["Status"] == "Outdated":
            status_class = "pico-color-orange-500"
        elif data["Status"] == "OK":
            status_class = "pico-color-green-500"
        return status_class

    def write_report(self):
        self.report += self.report_header

        production_section = self._heading("Production Dependencies")
        production_section += self._open_table("striped")
        production_section += self._table_header(["Package", "Installed Version", "Latest Version", "Status"])
        for data in self.production_data:
            production_section += self._table_dependency_row(data, self._gather_status_class(data))
        production_section += self._close_table()
        self.report += "<section><div class='container'>" + production_section + "</div></section>"

        self.report += "<hr>"

        development_section = self._heading("Development Dependencies")
        development_section += self._open_table("striped")
        development_section += self._table_header(["Package", "Installed Version", "Latest Version", "Status"])
        for data in self.development_data:
            development_section += self._table_dependency_row(data, self._gather_status_class(data))
        development_section += self._close_table()
        self.report += "<section><div class='container'>" + development_section + "</div></section>"

        self.report += "<hr>"

        info_section = self._heading("Branch Information")
        info_section += self._open_table("striped")
        for key, value in self.info_data.items():
            info_section += f"<tr><th>{key}</th><td>{value}</td></tr>"
        info_section += self._close_table()
        self.report += "<section><div class='container'>" + info_section + "</div></section>"

        self.report += "<hr>"

        self.report += self.report_footer

        with open("report.html", "w") as f:
            f.write(self.report)
