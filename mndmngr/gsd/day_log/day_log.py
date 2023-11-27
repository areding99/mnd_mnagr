from typing import NamedTuple
from mndmngr.gsd.task.task import Task


class DLHeader(NamedTuple):
    title: str
    path: str
    created: str
    id: str


class DLTasksSection(NamedTuple):
    tasks: list[tuple[Task, bool]]


# todos live as a part of the daylog - they don't exist outside this context
class DLTodosSection(NamedTuple):
    existing: list[tuple[str, bool]]
    new_today: list[tuple[str, bool]]


class DLSummarySection(NamedTuple):
    notes: str
    today_summary: str
    yesterday_summary: str


class DayLog:
    def __init__(
        self,
        header: DLHeader,
        tasks: DLTasksSection,
        todos: DLTodosSection,
        summary: DLSummarySection,
    ) -> None:
        self.header = header
        self.tasks = tasks
        self.todos = todos
        self.summary = summary
