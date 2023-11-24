import os

if __name__ == "__main__":
    import dotenv, sys

    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])

from mndmngr.gsd.task_and_todo.task.task import Task
from mndmngr.gsd.task_and_todo.task.db_driver.lib.parsing import parse_task
from mndmngr.config.config_parser import ConfigParser, Config


def _query_raw_task_by_id(id: str) -> list[str] | None:
    cwd = os.getcwd()

    os.chdir(os.environ["TASKS_PATH"])

    for section in os.listdir():
        os.chdir(section)
        print(section)
        for task_file in os.listdir():
            with open(task_file, "r") as f_io:
                for line in f_io.readlines():
                    # stop scanning after seeing first instance of 'id:' in metadata
                    if "id:" in line:
                        if id in line:
                            os.chdir(cwd)
                            f_io.seek(0)
                            return f_io.readlines()
                        continue
        os.chdir("..")

    os.chdir(cwd)
    return None


def _query_raw_tasks_in_section(section: str) -> list[list[str]]:
    cwd = os.getcwd()

    os.chdir(os.environ["TASKS_PATH"])
    os.chdir(section)

    tasks: list[list[str]] = []

    for t_file in os.listdir():
        with open(t_file, "r") as f_io:
            tasks.append(f_io.readlines())

    os.chdir(cwd)

    return tasks


def query_all_tasks_by_section() -> dict[str, list[Task]]:
    config: Config | None = ConfigParser().get_config()

    if not config:
        return {}

    sections: list[str] = config.tasks.task_subdirs_ordered
    sections_with_tasks: dict[str, list[Task]] = {}

    for section in sections:
        for task in _query_raw_tasks_in_section(section):
            if section not in sections_with_tasks:
                sections_with_tasks[section] = []
            sections_with_tasks[section].append(parse_task(task))

    return sections_with_tasks
