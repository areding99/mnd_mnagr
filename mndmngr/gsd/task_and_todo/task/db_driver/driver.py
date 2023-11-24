import mndmngr.gsd.task_and_todo.task.db_driver.read as read_driver
from types import ModuleType


def read() -> ModuleType:
    return read_driver
