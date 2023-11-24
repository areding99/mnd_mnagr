import os
import re
import dotenv
import questionary
import datetime
import uuid
from typing import Any, NamedTuple

if __name__ == "__main__":
    import sys

    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])

from mndmngr.gsd.task_and_todo.task.task import Task, TaskMetadata, TaskAbout
from mndmngr.config.config_parser import ConfigParser, Config
from mndmngr.lib.typing.is_list_of_str import is_list_of_str


class TaskCLIInput(NamedTuple):
    title: str
    section: str
    requestor: str
    subscribers: list[str]
    status: str
    urgency: str
    priority: str
    tags: list[str]
    due: str
    overview: str


def prompt_for_task_creation() -> dict[str, list[str] | str]:
    sections = []
    status = []
    urgency = []
    priority = []
    tags = []

    config: Config | None = ConfigParser().get_config()

    if config:
        sections = config.tasks.task_subdirs_ordered
        status = config.tasks.task_config.status
        urgency = config.tasks.task_config.urgency
        priority = config.tasks.task_config.priority
        tags = config.tasks.task_config.tags

    questions: list[dict[str, Any]] = [
        {"type": "text", "message": "enter a title for the task", "name": "title"},
        {
            "type": "select",
            "message": "select a section for the task",
            "name": "section",
            "choices": sections,
        }
        if len(sections) > 0
        else {
            "type": "text",
            "message": "Select a section for the task",
            "name": "section",
        },
        {"type": "text", "message": "who requested the task?", "name": "requestor"},
        {
            "type": "text",
            "message": "who is subscribed to this task?",
            "name": "subscribers",
        },
        {
            "type": "select",
            "message": "what is the status of this task?",
            "name": "status",
            "choices": status,
        }
        if len(status) > 0
        else {
            "type": "text",
            "message": "what is the status of this task?",
            "name": "status",
        },
        {
            "type": "select",
            "message": "how urgent is this task?",
            "name": "urgency",
            "choices": urgency,
        }
        if len(urgency) > 0
        else {"type": "text", "message": "how urgent is this task?", "name": "urgency"},
        {
            "type": "select",
            "message": "what is the priority of this task?",
            "name": "priority",
            "choices": priority,
        }
        if len(priority) > 0
        else {
            "type": "text",
            "message": "what is the priority of this task?",
            "name": "priority",
        },
        {
            "type": "checkbox",
            "message": "select applicable tags",
            "name": "tags",
            "choices": tags,
        }
        if len(sections) > 0
        else {"type": "text", "message": "tag this task", "name": "tags"},
        {
            "type": "text",
            "message": "due date?",
            "name": "due",
            "validate": lambda val: (
                re.match(
                    r"((?:19|20)\d\d)-(0[1-9]|1[012])-([12][0-9]|3[01]|0[1-9])", val
                )
                != None
                or val == ""
            )
            or "date must be in the format YYYY-MM-DD",
        },
        {"type": "text", "message": "what's this task about?", "name": "overview"},
    ]

    return questionary.prompt(questions)


def parse_task_creation_input(raw_input: dict[str, list[str] | str]) -> TaskCLIInput:
    title: str = ""
    if isinstance(raw_input["title"], str):
        title = raw_input["title"]

    section: str = ""
    if isinstance(raw_input["section"], str):
        section = raw_input["section"]

    requestor: str = ""
    if isinstance(raw_input["requestor"], str):
        requestor = raw_input["requestor"]

    subscribers: list[str] = []
    if is_list_of_str(raw_input["subscribers"]):
        subscribers = raw_input["subscribers"]

    status: str = ""
    if isinstance(raw_input["status"], str):
        status = raw_input["status"]

    urgency: str = ""
    if isinstance(raw_input["urgency"], str):
        urgency = raw_input["urgency"]

    priority: str = ""
    if isinstance(raw_input["priority"], str):
        priority = raw_input["priority"]

    tags: list[str] = []
    if is_list_of_str(raw_input["tags"]):
        tags = raw_input["tags"]

    due: str = ""
    if isinstance(raw_input["due"], str):
        due = raw_input["due"]

    overview: str = ""
    if isinstance(raw_input["overview"], str):
        overview = raw_input["overview"]

    return TaskCLIInput(
        title,
        section,
        requestor,
        subscribers,
        status,
        urgency,
        priority,
        tags,
        due,
        overview,
    )


def create_task_from_cli() -> Task:
    raw_input = prompt_for_task_creation()
    parsed_input = parse_task_creation_input(raw_input)

    metadata = TaskMetadata(
        parsed_input.title,
        os.environ["TASKS_REL_PATH"] + parsed_input.section,
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        str(uuid.uuid4()),
    )

    about_section = TaskAbout(
        parsed_input.requestor,
        parsed_input.subscribers,
        parsed_input.status,
        parsed_input.urgency,
        parsed_input.priority,
        parsed_input.tags,
        parsed_input.due,
    )

    return Task(metadata, about_section, [parsed_input.overview])


def create_task_from_cli_and_persist() -> Task:
    task = create_task_from_cli()
    task.persist()
    return task


create_task_from_cli_and_persist()
