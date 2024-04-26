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

    def write_report(self):
        self.report += self.report_header

        info_section = "<h2>Info</h2>\n"
        info_section += "<table class='striped'>\n"
        for key, value in self.info_data.items():
            info_section += f"<tr><th>{key}</th><td>{value}</td></tr>"
        info_section += "</table>"
        self.report += "<section><div class='container'>" + info_section + "</div></section>"

        self.report += "<hr>"

        production_section = "<h2>Production Dependencies</h2>"
        production_section += "<table class='striped'>"
        production_section += (
            "<thead><tr><th>Package</th><th>Installed Version</th><th>Latest Version</th><th>Status</th></tr></thead>"
        )
        for data in self.production_data:
            status_class = "pico-color-red-500"
            if data["Status"] == "Check":
                status_class = "pico-color-cyan-500"
            elif data["Status"] == "Outdated":
                status_class = "pico-color-orange-500"
            elif data["Status"] == "OK":
                status_class = "pico-color-green-500"
            production_section += f"<tr><td><span class='{status_class}'>{data['Package']}</span></td><td>{data['Installed Version']}</td><td>{data['Latest Version']}</td><td><span class='{status_class}'>{data['Status']}</span></td></tr>"  # noqa
        production_section += "</table>"
        self.report += "<section><div class='container'>" + production_section + "</div></section>"

        self.report += "<hr>"

        development_section = "<h2>Development Dependencies</h2>"
        development_section += "<table class='striped'>"
        development_section += (
            "<thead><tr><th>Package</th><th>Installed Version</th><th>Latest Version</th><th>Status</th></tr></thead>"
        )
        for data in self.development_data:
            status_class = "pico-color-red-500"
            if data["Status"] == "Check":
                status_class = "pico-color-cyan-500"
            elif data["Status"] == "Outdated":
                status_class = "pico-color-orange-500"
            elif data["Status"] == "OK":
                status_class = "pico-color-green-500"
            development_section += f"<tr><td><span class='{status_class}'>{data['Package']}</span></td><td>{data['Installed Version']}</td><td>{data['Latest Version']}</td><td><span class='{status_class}'>{data['Status']}</span></td></tr>"  # noqa
        development_section += "</table>"
        self.report += "<section><div class='container'>" + development_section + "</div></section>"

        self.report += "<hr>"

        self.report += self.report_footer

        with open("report.html", "w") as f:
            f.write(self.report)
