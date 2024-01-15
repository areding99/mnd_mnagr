from typing import TypeGuard

from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity


def is_list_of_task(obj: object) -> TypeGuard[list[TaskDBEntity]]:
    return isinstance(obj, list) and all(isinstance(i, TaskDBEntity) for i in obj)
