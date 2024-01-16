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

from mndmngr.config.config_parser import ConfigParser, Config
from mndmngr.lib.typing.is_list_of_str import is_list_of_str
from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity
from mndmngr.gsd.data.entities.Task.TaskEntityData import TaskEntityData
from mndmngr.gsd.data.entities.Task.TaskDBEntityWriter import TaskDBEntityWriter
from mndmngr.gsd.data.entities.Task.convenience.task_exists_at import task_exists_at
import mndmngr.gsd.data.EntityManager as EntityManager


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


def get_task_creation_questions() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
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

    if len(sections) == 0:
        print("no sections found for task storage - please specify in config")
        exit(1)

    metadata_questions: list[dict[str, Any]] = [
        {
            "type": "text",
            "message": "enter a title for the task",
            "name": "title",
            "validate": lambda val: (
                (len(re.findall(r"(\s|\/)", val)) == 0 and val != "")
            )
            or "enter a valid title (no whitespace or '/' characters)",
        },
        {
            "type": "select",
            "message": "select a section for the task",
            "name": "section",
            "choices": sections,
        },
    ]

    content_questions: list[dict[str, Any]] = []

    content_questions.append(
        {"type": "text", "message": "who requested the task?", "name": "requestor"}
    )
    content_questions.append(
        {
            "type": "text",
            "message": "who is subscribed to this task?",
            "name": "subscribers",
        }
    )

    if len(status) > 0:
        content_questions.append(
            {
                "type": "select",
                "message": "what is the status of this task?",
                "name": "status",
                "choices": status,
            }
        )
    if len(urgency) > 0:
        content_questions.append(
            {
                "type": "select",
                "message": "how urgent is this task?",
                "name": "urgency",
                "choices": urgency,
            }
        )
    if len(priority) > 0:
        content_questions.append(
            {
                "type": "select",
                "message": "what is the priority of this task?",
                "name": "priority",
                "choices": priority,
            }
        )
    if len(tags) > 0:
        content_questions.append(
            {
                "type": "checkbox",
                "message": "select applicable tags",
                "name": "tags",
                "choices": tags,
            }
        )
    content_questions.append(
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
        }
    )
    content_questions.append(
        {"type": "text", "message": "what's this task about?", "name": "overview"}
    )

    return (metadata_questions, content_questions)


def prompt_for_task_creation_input() -> dict[str, list[str] | str]:
    metadata_questions, content_questions = get_task_creation_questions()

    valid_input: bool = False

    while not valid_input:
        raw_input = questionary.prompt(metadata_questions)

        title: str = ""
        if isinstance(raw_input["title"], str):
            title = raw_input["title"]

        section: str = ""
        if isinstance(raw_input["section"], str):
            section = raw_input["section"]

        if title == "" or section == "":
            print("title and section are required")
            continue

        if task_exists_at(section + "/" + title):
            print("task already exists in " + section + " dir; try a new name")
            continue

        valid_input = True

    raw_input.update(questionary.prompt(content_questions))

    return raw_input


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


def create_task_from_cli() -> None:
    raw_input = prompt_for_task_creation_input()
    parsed_input = parse_task_creation_input(raw_input)

    data = TaskEntityData(
        parsed_input.title,
        TaskDBEntity.get_entity_path_rel()
        + "/"
        + parsed_input.section
        + "/"
        + parsed_input.title
        + ".md",
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        str(uuid.uuid4()),
        parsed_input.requestor,
        parsed_input.subscribers,
        parsed_input.status,
        parsed_input.urgency,
        parsed_input.tags,
        parsed_input.priority,
        parsed_input.due,
        [parsed_input.overview],
    )

    task = TaskDBEntity(data.path, data)
    created = EntityManager.write(task, TaskDBEntityWriter())

    if created:
        print("task created at: " + task.get_path())
    else:
        print("task creation failed")
