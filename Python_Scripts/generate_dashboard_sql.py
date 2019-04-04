import os
import xml.etree.ElementTree


OSCARDOC_PROVIDER_NO = "999998"
DASHBOARD_NAMES = [
    "Panel Mgmt 1 - Active Pts, Assigned Provider, Pt Contact Info, Polypharm, Advance Care Planning, Frailty",
    "Panel Mgmt 2 - BP, CHF, DM, COPD, CKD, Ischemic Heart dz, Liver dz, Cerebrovasc dz",
    "Panel Mgmt 3 - OA, Chronic Pain, Anxiety, Depression, Drug and Alcohol Dependence, Dementia",
    "Panel Mgmt Reports -Pop Histogram, Aggregate Spreadsheets for Pt Contact and Primary Provider",
    "Panel Tools"
]

TEMPLATE_FILENAME = "DoBC_dashboard_template.sql"
OUTPUT_FILENAME = "DoBC_dashboard.sql"

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Indicator(object):
    def __init__(self, name, category, sub_category,
                 framework, framework_version,
                 definition, notes, template):
        self.name = name
        self.category = category
        self.sub_category = sub_category
        self.framework = framework
        self.framework_version = framework_version
        self.definition = definition
        self.notes = notes
        self.template = template


class Dashboard(object):
    def __init__(self, name):
        self.name = name
        self.indicators = []

    def add_indicator(self, indicator):
        self.indicators.append(indicator)

    def get_indicators(self):
        return self.indicators


class IndicatorParser(object):
    def _check_not_none(self, value, value_name):
        if value is None:
            raise ValueError(
                "Indicator {} cannot be None".format(value_name)
            )

    def parse_indicator(self, filehandle):
        template = filehandle.read()
        self._check_not_none(template, "template")

        root = xml.etree.ElementTree.fromstring(template)

        def parse_text(xpath):
            return root.find(xpath).text

        name = parse_text("./heading/name")
        self._check_not_none(name, "name")

        category = parse_text("./heading/category")
        self._check_not_none(category, "category")

        sub_category = parse_text("./heading/subCategory")
        self._check_not_none(sub_category, "subCategory")

        framework = parse_text("./heading/framework")
        framework_version = parse_text("./heading/frameworkVersion")

        definition = parse_text("./heading/definition") or ""
        notes = parse_text("./heading/notes") or ""

        return Indicator(
            name, category, sub_category,
            framework, framework_version,
            definition, notes, template
        )


class SQLGenerator(object):
    def generate_indicator_insert_statement(self, indicator, dashboard_id):
        def escape_special_characters(string):
            string = string.replace("\"", "\\\"")
            string = string.replace("'", "\\'")
            return string

        sql = (
            "INSERT INTO `indicatorTemplate` (`dashboardId`, "
            "`name`, `category`, `subCategory`, `framework`, "
            "`frameworkVersion`, `definition`, `notes`, `template`, "
            "`active`, `locked`, `shared`, `metricSetName`, `metricLabel`) "
            "VALUES ({},'{}','{}','{}','{}','{}','{}','{}','{}',"
            "'','\\0',0,NULL,NULL);"
        ).format(
            dashboard_id,
            indicator.name, indicator.category, indicator.sub_category,
            indicator.framework, indicator.framework_version,
            escape_special_characters(indicator.definition),
            escape_special_characters(indicator.notes),
            escape_special_characters(indicator.template.decode("utf-8"))
        )

        sql = sql.replace("\n", "\\n")

        return sql

    def generate_dashboard_sql(self, dashboards):
        with open(os.path.join(SCRIPT_DIRECTORY, TEMPLATE_FILENAME), "r") as filehandle:
            template = filehandle.read()

        # TODO more efficient?
        insert_statements = ""
        for index, dashboard in enumerate(dashboards):
            dashboardId = "@dashboardId{}".format(index + 1)

            insert_statements += "\n".join(
                self.generate_indicator_insert_statement(indicator, dashboardId)
                for indicator in dashboard.get_indicators()
            )
            insert_statements += "\n"

        insert_statements = insert_statements.rstrip()

        return template.format(
            oscardoc_provider_no=OSCARDOC_PROVIDER_NO,
            indicator_insert_statements=insert_statements
        )


class IndicatorRepository(object):
    """
    Used to access info about indicators in this repository.
    """
    def __init__(self):
        self.root_directory = os.path.dirname(SCRIPT_DIRECTORY)

    def get_dashboard_names(self):
        return DASHBOARD_NAMES

    def get_indicator_paths(self, dashboard):
        indicator_paths = []

        dashboard_directory = os.path.join(self.root_directory, dashboard)
        for filename in sorted(os.listdir(dashboard_directory)):
            if filename.endswith("xml"):
                indicator_path = os.path.join(dashboard_directory, filename)
                indicator_paths.append(indicator_path)

        return indicator_paths


def main():
    indicator_repository = IndicatorRepository()
    dashboard_names = indicator_repository.get_dashboard_names()

    parser = IndicatorParser()
    dashboards = []

    for dashboard_name in dashboard_names:
        dashboard = Dashboard(dashboard_name)

        indicator_paths = indicator_repository.get_indicator_paths(dashboard_name)
        for path in indicator_paths:
            with open(path, "rb") as indicator_filehandle:
                indicator = parser.parse_indicator(indicator_filehandle)
                dashboard.add_indicator(indicator)

        dashboards.append(dashboard)

    sql_generator = SQLGenerator()
    dashboard_sql = sql_generator.generate_dashboard_sql(dashboards)

    output_filepath = os.path.join(SCRIPT_DIRECTORY, OUTPUT_FILENAME)
    with open(output_filepath, "w") as filehandle:
        filehandle.write(dashboard_sql)

    print("Generated {}".format(output_filepath))


if __name__ == "__main__":
    main()
