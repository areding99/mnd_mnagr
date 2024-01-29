from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity
from mndmngr.gsd.data.entities.Task.TaskDBEntityDataParser import TaskDBEntityDataParser
import mndmngr.gsd.data.EntityManager as EntityManager
from mndmngr.gsd.data.entities.Task.TaskDBEntityWriter import TaskDBEntityWriter


def set_task_status(task: TaskDBEntity, status: str) -> None:
    if not task.is_initialized():
        EntityManager.initialize(task, TaskDBEntityDataParser())

    if not task.is_initialized():
        raise Exception("failed to initialize task")

    data = task.get_data()
    if data is None:
        raise Exception("data cannot be None if task is initialized")

    data.status = status
    EntityManager.write(task, TaskDBEntityWriter())

    return None
