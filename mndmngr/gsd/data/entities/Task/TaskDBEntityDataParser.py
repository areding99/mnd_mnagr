import re
from mndmngr.gsd.data.entities.IDBEntityDataParser import IDBEntityDataParser
from mndmngr.gsd.data.entities.Task.TaskEntityData import TaskEntityData


class TaskDBEntityDataParser(IDBEntityDataParser):
    def parse(self, data: list[str]) -> TaskEntityData:
        metadata_section: list[str] = []
        in_metadata: bool = False
        about_section: list[str] = []
        in_about: bool = False

        for line in data:
            # metadata section -----------------
            if line.startswith("---"):
                in_metadata = False

            if in_metadata:
                metadata_section.append(line)
                # sanity check: one section at a time
                continue

            if line.startswith("---") and len(metadata_section) == 0:
                in_metadata = True
                # sanity check: one section at a time
                continue

            # about section -----------------
            if line == "\n" and in_about:
                break

            if in_about:
                about_section.append(line)
                continue

            if re.match(r"(\|\s*-+\s*){2}\|", line) and len(about_section) == 0:
                in_about = True

        metadata = _parse_metadata_section(metadata_section)
        about = _parse_about_section(about_section)

        return _collate_parsed_sections(metadata, about, data)


def _parse_metadata_section(section: list[str]) -> dict[str, str]:
    parsed = {}

    parsed["title"] = ""
    parsed["path"] = ""
    parsed["created"] = ""
    parsed["id"] = ""

    for line in section:
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


def _parse_about_section(section: list[str]) -> dict[str, str | list[str]]:
    parsed: dict[str, str | list[str]] = {}

    parsed["requestor"] = ""
    parsed["subscribers"] = []
    parsed["status"] = ""
    parsed["urgency"] = ""
    parsed["priority"] = ""
    parsed["tags"] = []
    parsed["due"] = ""

    for line in section:
        l = re.split(r"\|", line)
        key = l[1].strip()
        val = l[2].strip()

        match key:
            case "requestor":
                parsed["requestor"] = val
            case "subscribers":
                sub_list = []
                for v in val.split(","):
                    sub_list.append(v.strip())
                parsed["subscribers"] = sub_list
            case "status":
                parsed["status"] = val
            case "urgency":
                parsed["urgency"] = val
            case "priority":
                parsed["priority"] = val
            case "tags":
                tag_list = []
                for v in val.split(","):
                    tag_list.append(v.strip())
                parsed["tags"] = tag_list
            case "due":
                parsed["due"] = val

    return parsed


def _collate_parsed_sections(
    metadata: dict[str, str], about: dict[str, str | list[str]], raw: list[str]
) -> TaskEntityData:
    return TaskEntityData(
        title=metadata["title"],
        path=metadata["path"],
        created=metadata["created"],
        id=metadata["id"],
        requestor=type(about["requestor"]) is str and about["requestor"] or "",
        subscribers=type(about["subscribers"]) is list and about["subscribers"] or [],
        status=type(about["status"]) is str and about["status"] or "",
        urgency=type(about["urgency"]) is str and about["urgency"] or "",
        tags=type(about["tags"]) is list and about["tags"] or [],
        priority=type(about["priority"]) is str and about["priority"] or "",
        due=type(about["due"]) is str and about["due"] or "",
        body=raw,
    )
