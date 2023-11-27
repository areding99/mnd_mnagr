import os
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
        full_task_path = os.environ["PROJECT_ROOT"] + self.metadata.path

        with open(full_task_path, "w+") as f_io:
            f_io.writelines("hello from task")

        return None


# for now, even though tasks have a uuid, use path as unique identifier for readablility in files
class TaskRef:
    def __init__(self, path: str) -> None:
        self.path = path

    def __repr__(self) -> str:
        return "(TaskRef)" + self.path

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TaskRef):
            return NotImplemented
        return self.path == other.path

    def __hash__(self) -> int:
        return hash(self.path)
