import os
import re
import sys

import dotenv

if __name__ == "__main__":
    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])


def get_first_md_link_path(line: str) -> str | None:
    match = re.search(r"\[.*\]\((.*)\)", line)

    if match:
        return match.group(1)

    return None


def is_incomplete_md_todo_item(line: str) -> bool:
    return line.startswith("- [ ]")


def strip_md_todo_item(line: str) -> str:
    return line[5:].strip()
