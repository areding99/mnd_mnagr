import datetime, uuid, os
from typing import NamedTuple


class TaskMetadata(NamedTuple):
    title: str
    path: str
    created: str
    id: str


class TaskAbout(NamedTuple):
    requestor: str
    subscribers: list[str]
    status: str
    urgency: str
    priority: str
    tags: list[str]
    due: str


class Task:
    def __init__(
        self, metadata: TaskMetadata, about_section: TaskAbout, raw_task: list[str]
    ) -> None:
        self.metadata = metadata
        self.about_section = about_section
        self.raw_task = raw_task

    def persist(self) -> None:
        with open(os.environ["PROJECT_ROOT"] + self.metadata.path) as f_io:
            f_io.writelines("hello from task")

        return None
