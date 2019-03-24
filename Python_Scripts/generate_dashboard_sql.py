import collections
import json
import os
import xml.etree.ElementTree


CONFIG_FILENAME = "config.json"
TEMPLATE_FILENAME = "DoBC_dashboard_template.sql"
SCRIPT_DIRECTORY = os.path.dirname(__file__)


class Indicator(object):
    def __init__(self, name, category, sub_category,
                 framework, framework_version,
                 definition, notes, template):
        self.name = name
        self.category = category
        self.sub_category = sub_category
        self.framework = framework
        self.framework_version = framework_version
        self.definition = definition if definition is not None else ""
        self.notes = notes if notes is not None else ""
        self.template = template


class IndicatorParser(object):
    def parse_indicator(self, filehandle):
        tree = xml.etree.ElementTree.parse(filehandle)
        root = tree.getroot()

        def parse_text(xpath):
            return root.find(xpath).text

        name = parse_text("./heading/name")
        category = parse_text("./heading/category")
        sub_category = parse_text("./heading/subCategory")
        framework = parse_text("./heading/framework")
        framework_version = parse_text("./heading/frameworkVersion")
        definition = parse_text("./heading/definition")
        notes = parse_text("./heading/notes")
        template = xml.etree.ElementTree.tostring(root, encoding="utf-8")

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
            "'','\0',0,NULL,NULL);"
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

    def generate_dashboard_sql(self, dashboard_indicators):
        with open(os.path.join(SCRIPT_DIRECTORY, TEMPLATE_FILENAME), "r") as filehandle:
            template = filehandle.read()

        # TODO more efficient?
        insert_statements = ""
        for dashboard in dashboard_indicators:
            for indicator in dashboard_indicators[dashboard]:
                # TODO: real dashboard ID
                insert_statements += "\n" + self.generate_indicator_insert_statement(indicator, "@dashboardId1")

        return template.format(indicator_insert_statements=insert_statements)


class IndicatorRepository(object):
    def __init__(self):
        self.root_directory = os.path.dirname(SCRIPT_DIRECTORY)

        config_filepath = os.path.join(SCRIPT_DIRECTORY, CONFIG_FILENAME)
        with open(config_filepath, "r") as filehandle:
            self.config_data = json.load(filehandle)

    def get_dashboard_names(self):
        return self.config_data["dashboards"]

    def get_indicator_paths(self, dashboard):
        indicator_paths = []

        dashboard_directory = os.path.join(self.root_directory, dashboard)
        for filename in os.listdir(dashboard_directory):
            if filename.endswith("xml"):
                indicator_path = os.path.join(dashboard_directory, filename)
                indicator_paths.append(indicator_path)

        return indicator_paths


def main():
    indicator_repository = IndicatorRepository()
    dashboards = indicator_repository.get_dashboard_names()

    # TODO preserve order
    dashboard_indicators = collections.defaultdict(list)

    parser = IndicatorParser()
    for dashboard in dashboards:
        indicator_paths = indicator_repository.get_indicator_paths(dashboard)
        for path in indicator_paths:
            with open(path, "rb") as indicator_filehandle:
                indicator = parser.parse_indicator(indicator_filehandle)
                dashboard_indicators[dashboard].append(indicator)

    sql_generator = SQLGenerator()
    dashboard_sql = sql_generator.generate_dashboard_sql(dashboard_indicators)

    # TODO write to file so we can have info printouts
    print(dashboard_sql)


if __name__ == "__main__":
    main()
