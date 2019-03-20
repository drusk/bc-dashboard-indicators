import collections
import json
import os


CONFIG_FILENAME = "config.json"


class Indicator(object):
    def __init__(self, name, category, sub_category, framework, framework_version, definition, notes, template, active, locked, shared):
        pass


class IndicatorParser(object):
    def parse_indicator(self, filehandle):
        return Indicator()


class SQLGenerator(object):
    def generate_indicator_insert_statement(self, indicator):
        return ""


class SQLWriter(object):
    def write(self, indicators, output_filehandle):
        pass


class IndicatorRepository(object):
    def __init__(self):
        self.script_directory = os.path.dirname(__file__)
        self.root_directory = os.path.dirname(self.script_directory)

        config_filepath = os.path.join(self.script_directory, CONFIG_FILENAME)
        with open(config_filepath, "r") as filehandle:
            self.config_data = json.load(filehandle)

    def get_dashboard_names(self):
        return self.config_data["dashboards"]

    def get_indicator_paths(self, dashboard):
        indicator_paths = []

        dashboard_directory = os.path.join(self.root_directory, dashboard)
        for filename in os.listdir(dashboard_directory):
            indicator_path = os.path.join(dashboard_directory, filename)
            indicator_paths.append(indicator_path)

        return indicator_paths


def main():
    indicator_repository = IndicatorRepository()
    dashboards = indicator_repository.get_dashboard_names()

    dashboard_indicators = collections.defaultdict(list)

    parser = IndicatorParser()
    for dashboard in dashboards:
        print(dashboard)
        indicator_paths = indicator_repository.get_indicator_paths(dashboard)
        for path in indicator_paths:
            print(path)
            #with open(path, "rb") as indicator_filehandle:
                #indicator = parser.parse_indicator(indicator_filehandle)
                #dashboard_indicators[dashboard].append(indicator)


if __name__ == "__main__":
    main()
