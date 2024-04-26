from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class HTMLReporter:
    report_header: str = ""
    report_footer: str = ""
    report_body: str = ""

    report_info: dict = None
    report_production: dict = None
    report_development: dict = None

    def __post_init__(self):
        with open("report_header.html") as f:
            self.report_header = f.read()

        with open("report_footer.html") as f:
            self.report_footer = f.read()

    def write_report(self):
        with open("report.html", "w") as f:
            f.write(self.report_header)
            f.write(self.report_body)
            f.write(self.report_footer)

    def generate_info_report(self, data: DataFrame):
        self.report_body = "<h1>Info Report</h1>"

        self.report_info = data.describe().to_html()
        self.report_body += f"<p>{self.report_info}</p>"
