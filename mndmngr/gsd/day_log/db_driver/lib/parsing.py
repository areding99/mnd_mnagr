import os, re, sys, dotenv
from mndmngr.config.config_parser import ConfigParser

from mndmngr.gsd.task.task import Task
from mndmngr.lib.parsing.utils import get_first_md_link_path, is_incomplete_md_todo_item

if __name__ == "__main__":
    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])


from mndmngr.gsd.day_log.day_log import (
    DLHeader,
    DLTasksSection,
    DLTodosSection,
    DLSummarySection,
    DayLog,
)


# IMPLEMENT the following as next step (can test in read.py)
def _parse_header(section: list[str]) -> DLHeader:
    title: str = ""
    path: str = ""
    created: str = ""
    id: str = ""

    for line in section:
        l = re.split(r":", line, 1)
        key = l[0].strip()
        val = l[1].strip()

        match key:
            case "title":
                title = val
            case "path":
                path = val
            case "created":
                created = val
            case "id":
                id = val

    return DLHeader(title, path, created, id)


# get the tasks as they appear in the daylog, not as they would be generated for the daylog
def _parse_tasks_section(tasks_section: list[str]) -> DLTasksSection | None:
    sections_w_tasks: dict[str, list[tuple[Task, bool]]]

    config = ConfigParser().get_config()

    if not config:
        print("could not find config")
        return None

    subsection_delim = config.daylog.subsection_delimiter

    section_name = ""

    for line in tasks_section:
        if line.startswith(subsection_delim):
            section_name = line[len(subsection_delim) :].strip()
            continue

        if line.startswith("-"):
            path = get_first_md_link_path(line)

            if not path:
                print("task path not found")
                return None

            task_ref = Task(path)
            sections_w_tasks[section_name].append(
                (task_ref, is_incomplete_md_todo_item(line))
            )

    return DLTasksSection(sections_w_tasks)


def _parse_todos_section(section: list[str]) -> DLTodosSection | None:
    return None


def _parse_summary_section(section: list[str]) -> DLSummarySection | None:
    return None


def parse_day_log(raw_dl: list[str]) -> DayLog | None:
    raw_header: list[str] = []
    raw_tasks_section: list[str] = []
    raw_todos_section: list[str] = []
    raw_summary_section: list[str] = []

    in_header: bool = False
    in_tasks_section: bool = False
    in_todos_section: bool = False
    in_summary_section: bool = False

    for line in raw_dl:
        # header -----------------
        if line.startswith("---"):
            in_header = False

        if in_header:
            raw_header.append(line)
            # sanity check; one section at a time
            continue

        if line.startswith("---") and len(raw_header) == 0:
            in_header = True
            # sanity check; one section at a time
            continue

        # body (tasks -> todos -> summary) -----------------
        # TODO update to use config delimiters
        if line.startswith("# tasks"):
            in_tasks_section = True
            continue

        if line.startswith("# todos"):
            in_tasks_section = False
            in_todos_section = True
            continue

        if in_tasks_section:
            raw_tasks_section.append(line)
            continue

        if line.startswith("# summary"):
            in_todos_section = False
            in_summary_section = True
            continue

        if in_todos_section:
            raw_todos_section.append(line)
            continue

        if in_summary_section:
            raw_summary_section.append(line)

    # print("HEADER: \n")
    # print(raw_header)
    # print("\n\nTASKS: \n")
    # print(raw_tasks_section)
    # print("\n\nTODOS: \n")
    # print(raw_todos_section)
    # print("\n\nSUMMARY: \n")
    # print(raw_summary_section)

    clean_header = _parse_header(raw_header)

    print(clean_header)

    clean_tasks_section = _parse_tasks_section(raw_tasks_section)
    clean_todos_section = _parse_todos_section(raw_todos_section)
    clean_summary_section = _parse_summary_section(raw_summary_section)

    if not clean_tasks_section or not clean_todos_section or not clean_summary_section:
        return None

    return DayLog(
        clean_header,
        clean_tasks_section,
        clean_todos_section,
        clean_summary_section,
    )
