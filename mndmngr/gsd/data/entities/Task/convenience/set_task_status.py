from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity
from mndmngr.gsd.data.entities.Task.TaskDBEntityDataParser import TaskDBEntityDataParser
import mndmngr.gsd.data.EntityManager as EntityManager
from mndmngr.gsd.data.entities.Task.TaskDBEntityWriter import TaskDBEntityWriter
from mndmngr.gsd.data.entities.Task.TaskEntityData import TaskEntityData


def set_task_status(task: TaskDBEntity, status: str) -> None:
    if not task.is_initialized():
        EntityManager.initialize(task, TaskDBEntityDataParser())

    if not task.is_initialized():
        raise Exception("failed to initialize task")

    data = task.get_data()
    if not isinstance(data, TaskEntityData):
        # this is for mypy - is_intialized() is essentially a 'None' check
        raise Exception("failed to get task data")

    data.status = status
    EntityManager.write(task, TaskDBEntityWriter())

    return None
