import json, os
from typing import NamedTuple, Any, Self
from mndmngr.lib.typing.is_list_of_str import is_list_of_str


class Template(NamedTuple):
    name: str
    body: list[str]


class TemplateConfig(NamedTuple):
    templates: dict[str, Template]


REL_PATH_TO_TEMPLATE_CONFIG = "/mndmngr/pkm/templates/template_defs.json"


class TemplateConfigParser(object):
    _instance = None
    config: TemplateConfig | None = None

    def __new__(cls) -> Self:
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def get_config(self) -> TemplateConfig | None:
        if self.config is not None:
            return self.config

        with open(os.environ["MND_MNGR_ROOT"] + REL_PATH_TO_TEMPLATE_CONFIG) as f_io:
            self.config = TemplateConfigParser.parse_config(json.load(f_io))

        return self.config

    @staticmethod
    def parse_config(json: Any) -> TemplateConfig:
        if not json:
            raise Exception("config is empty")

        templates: dict[str, Template] = {}

        # iterate over the templates
        for item in json.items():
            name = item[1]["name"]
            body = item[1]["body"]

            if not isinstance(name, str):
                raise Exception("template name must be a string")

            if not is_list_of_str(body):
                raise Exception("template body must be a list of strings")

            templates[name] = Template(name, body)

        return TemplateConfig(templates)
