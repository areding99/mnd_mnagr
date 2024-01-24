import re


def get_first_md_link_path(line: str) -> str | None:
    match = re.search(r"\[.*\]\((.*)\)", line)

    if match:
        return match.group(1)

    return None


def is_incomplete_md_todo_item(line: str) -> bool:
    return line.startswith("- [ ]") or line.startswith("-[ ]")


def strip_md_todo_item(line: str) -> str:
    return line[5:].strip()
