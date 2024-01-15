import os
from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity


def get_task_sections() -> list[str]:
    path = TaskDBEntity.get_entity_path()
    subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    return subdirs
