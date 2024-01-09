import json
from typing import NamedTuple, Any, Self
from mndmngr.lib.typing.is_list_of_str import is_list_of_str


class DaylogConfig(NamedTuple):
    section_delimiter: str
    subsection_delimiter: str


class TaskConfig(NamedTuple):
    status: list[str]
    urgency: list[str]
    priority: list[str]
    tags: list[str]


class TasksSection(NamedTuple):
    task_config: TaskConfig
    task_subdirs_ordered: list[str]
    task_sort_order: list[str]


class Config(NamedTuple):
    daylog: DaylogConfig
    tasks: TasksSection


class ConfigParser(object):
    _instance = None
    config: Config | None = None

    def __new__(cls) -> Self:
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def get_config(self) -> Config | None:
        if self.config is not None:
            return self.config

        with open("./mndmngr/config/config.json") as f_io:
            self.config = ConfigParser.parse_config(json.load(f_io))

        return self.config

    @staticmethod
    def parse_config(config_json: Any) -> Config:
        if not config_json:
            raise Exception("config is empty")

        daylog_section_delimiter = config_json["daylog"]["section_delimiter"]
        if not isinstance(daylog_section_delimiter, str):
            raise Exception("config does not match expected format")

        daylog_subsection_delimiter = config_json["daylog"]["subsection_delimiter"]
        if not isinstance(daylog_subsection_delimiter, str):
            raise Exception("config does not match expected format")

        task_subdirs_ordered = config_json["tasks"]["task_subdirs_ordered"]
        if not is_list_of_str(task_subdirs_ordered):
            raise Exception("config does not match expected format")

        tasks_config_status_enum = config_json["tasks"]["task_config"]["status"]
        if not is_list_of_str(tasks_config_status_enum):
            raise Exception("config does not match expected format")

        tasks_config_urgency_enum = config_json["tasks"]["task_config"]["urgency"]
        if not is_list_of_str(tasks_config_urgency_enum):
            raise Exception("config does not match expected format")

        tasks_config_priority_enum = config_json["tasks"]["task_config"]["priority"]
        if not is_list_of_str(tasks_config_priority_enum):
            raise Exception("config does not match expected format")

        tasks_config_tags_enum = config_json["tasks"]["task_config"]["tags"]
        if not is_list_of_str(tasks_config_tags_enum):
            raise Exception("config does not match expected format")

        sort_order = config_json["tasks"]["task_sort_order"]
        if not is_list_of_str(sort_order):
            raise Exception("config does not match expected format")

        return Config(
            daylog=DaylogConfig(
                section_delimiter=daylog_section_delimiter,
                subsection_delimiter=daylog_subsection_delimiter,
            ),
            tasks=TasksSection(
                task_subdirs_ordered=task_subdirs_ordered,
                task_config=TaskConfig(
                    status=tasks_config_status_enum,
                    urgency=tasks_config_urgency_enum,
                    priority=tasks_config_priority_enum,
                    tags=tasks_config_tags_enum,
                ),
                task_sort_order=sort_order,
            ),
        )
