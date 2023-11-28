import os

from mndmngr.gsd.task.task import Task


def create_task(task: Task) -> Task | None:
    if not task.is_initialized():
        return None

    full_task_path = os.environ["PROJECT_ROOT"] + task.path

    if os.stat(full_task_path).st_size != 0:
        print("overwriting existing task")

    with open(full_task_path, "w+") as f_io:
        f_io.writelines("hello from task")

    return task
