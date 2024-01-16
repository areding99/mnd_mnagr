import re
from mndmngr.config.config_parser import ConfigParser
from mndmngr.gsd.data.entities.Daylog.DaylogEntityData import DaylogEntityData
from mndmngr.gsd.data.entities.IDBEntityDataParser import IDBEntityDataParser
from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity
from mndmngr.lib.parsing.utils import (
    get_first_md_link_path,
    is_incomplete_md_todo_item,
    strip_md_todo_item,
)


class DaylogDBEntityTaskFirstDataParser(IDBEntityDataParser):
    def parse(self, data: list[str]) -> DaylogEntityData:
        raw_metadata: list[str] = []
        raw_header: str = ""
        raw_tasks_section: list[str] = []
        raw_todos_section: list[str] = []
        raw_summary_section: list[str] = []

        in_metadata: bool = False
        seen_header: bool = False
        in_tasks_section: bool = False
        in_todos_section: bool = False
        in_summary_section: bool = False

        for line in data:
            # header -----------------
            if line.startswith("---"):
                in_metadata = False

            if in_metadata:
                raw_metadata.append(line)
                # sanity check; one section at a time
                continue

            if line.startswith("---") and len(raw_metadata) == 0:
                in_metadata = True
                # sanity check; one section at a time
                continue

            if line.startswith("# tasks"):
                # there is no header; skip this section & don't affect tasks parsing
                seen_header = True

            if line.startswith("#") and not seen_header:
                raw_header = line
                seen_header = True
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

        metadata = _parse_metadata_section(raw_metadata)
        header = _parse_header(raw_header)
        tasks = _parse_tasks_section(raw_tasks_section)
        todos = _parse_todos_section(raw_todos_section)
        summary = _parse_summary_section(raw_summary_section)

        return _collate_parsed_sections(metadata, header, tasks, todos, summary)


def _parse_header(raw: str) -> str:
    return raw[1:].strip()


def _parse_metadata_section(raw: list[str]) -> dict[str, str]:
    parsed = {}

    parsed["title"] = ""
    parsed["path"] = ""
    parsed["created"] = ""
    parsed["id"] = ""

    for line in raw:
        l = re.split(r":", line, 1)
        key = l[0].strip()
        val = l[1].strip()

        match key:
            case "title":
                parsed["title"] = val
            case "path":
                parsed["path"] = val
            case "created":
                parsed["created"] = val
            case "id":
                parsed["id"] = val

    return parsed


# retrieve the tasks as they appear in the daylog
def _parse_tasks_section(
    raw: list[str],
) -> dict[str, list[tuple[TaskDBEntity, bool]]]:
    tasks_by_section: dict[str, list[tuple[TaskDBEntity, bool]]] = {}

    config = ConfigParser().get_config()
    if not config:
        raise Exception("config not found")

    subsection_delim = config.daylog.subsection_delimiter

    section_name = ""

    for line in raw:
        if line.startswith(subsection_delim):
            section_name = line[len(subsection_delim) :].strip()
            tasks_by_section[section_name] = []
            continue

        if line.startswith("-"):
            path = get_first_md_link_path(line)

            if not path:
                print("task path not found")
                continue

            task_ref = TaskDBEntity(path)

            tasks_by_section[section_name].append(
                (task_ref, not is_incomplete_md_todo_item(line))
            )

    return tasks_by_section


def _parse_todos_section(raw: list[str]) -> dict[str, list[tuple[str, bool]]]:
    todos: dict[str, list[tuple[str, bool]]] = {}

    config = ConfigParser().get_config()
    if not config:
        raise Exception("config not found")

    subsection_delim = config.daylog.subsection_delimiter

    section_name = ""

    for line in raw:
        if line.startswith(subsection_delim):
            section_name = line[len(subsection_delim) :].strip()
            todos[section_name] = []

            continue

        if line.startswith("-"):
            todos[section_name].append(
                (strip_md_todo_item(line), not is_incomplete_md_todo_item(line))
            )

    return todos


def _parse_summary_section(raw: list[str]) -> dict[str, str]:
    parsed = {}

    parsed["notes"] = ""
    parsed["today_summary"] = ""
    parsed["yesterday_summary"] = ""

    in_notes = False
    in_today_summary = False
    in_yesterday_summary = False

    for line in raw:
        if line.startswith("## notes"):
            in_notes = True
            continue

        if line.startswith("## today"):
            in_notes = False
            in_today_summary = True
            continue

        if in_notes:
            parsed["notes"] += line.strip()
            continue

        if line.startswith("## yesterday"):
            in_today_summary = False
            in_yesterday_summary = True
            continue

        if in_today_summary:
            parsed["today_summary"] += line.strip()
            continue

        if in_yesterday_summary:
            parsed["yesterday_summary"] += line.strip()

    return parsed


def _collate_parsed_sections(
    metadata: dict[str, str],
    header: str,
    tasks: dict[str, list[tuple[TaskDBEntity, bool]]],
    todos: dict[str, list[tuple[str, bool]]],
    summary: dict[str, str],
) -> DaylogEntityData:
    return DaylogEntityData(
        title=metadata["title"],
        path=metadata["path"],
        created=metadata["created"],
        id=metadata["id"],
        header=header,
        tasks=tasks,
        todos=todos,
        notes=summary["notes"],
        today_summary=summary["today_summary"],
        yesterday_summary=summary["yesterday_summary"],
    )
