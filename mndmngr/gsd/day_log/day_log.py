from typing import NamedTuple
from mndmngr.gsd.task.task import Task
from mndmngr.gsd.todo.todo import Todo


class DLHeader(NamedTuple):
    title: str
    path: str
    created: str
    id: str


class DLTasksSection(NamedTuple):
    tasks: list[tuple[Task, bool]]


class DLTodosSection(NamedTuple):
    existing: list[tuple[Todo, bool]]
    new_today: list[tuple[Todo, bool]]


class DLASummarySection(NamedTuple):
    notes: str
    today_summary: str
    yesterday_summary: str


class DayLog:
    def __init__(
        self,
        header: DLHeader,
        tasks: DLTasksSection,
        todos: DLTodosSection,
        summary: DLASummarySection,
    ) -> None:
        self.header = header
        self.tasks = tasks
        self.todos = todos
        self.summary = summary
