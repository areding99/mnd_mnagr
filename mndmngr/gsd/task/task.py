from typing import NamedTuple, Self

import mndmngr.gsd.task.db_driver.driver as task_dbdriver


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


class TaskArgs(NamedTuple):
    metadata: TaskMetadata
    about: TaskAbout
    body: list[str]


class Task:
    # Task uses path as a unique identifier for it's availablity in md files
    def __init__(self, path: str, /, task_args: TaskArgs | None = None) -> None:
        self.path = path
        self.task_args = task_args

    def is_initialized(self) -> bool:
        return self.task_args is not None

    def __repr__(self) -> str:
        if self.is_initialized():
            return f"(Task)({self.path})"
        else:
            return f"(TaskRef)({self.path})"

    def load_safe(self) -> Self | None:
        if self.is_initialized():
            print(
                "task already initialized - loading from db will overwrite local state"
            )
            return None

        return self

    def _load_unsafe(self) -> Self:
        task_args = task_dbdriver.read().query_task_by_path(self.path)

        return Task(self.path, task_args)

    def persist(self) -> None:
        task_dbdriver.create().create_task(self)

        return None
