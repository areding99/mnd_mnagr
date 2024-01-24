import re
import pytest
import sys, dotenv, os

dotenv.load_dotenv()
sys.path.append(os.environ["MND_MNGR_ROOT"])

from mndmngr.gsd.data.entities.Daylog.DaylogEntityData import DaylogEntityData
from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity
from mndmngr.lib.parsing.utils import (
    get_first_md_link_path,
    is_incomplete_md_todo_item,
    strip_md_todo_item,
)


from mndmngr.gsd.data.entities.Daylog.DaylogDBEntityTaskFirstDataParser import (
    DaylogDBEntityTaskFirstDataParser,
    _parse_metadata_section,
    _parse_summary_section,
    _parse_tasks_section,
    _parse_todos_section,
)


###############
# SETUP
###############


# METADATA

METADATA_LINE_ZERO = "---"
METADATA_LINE_ONE = "title: 2023-11-20"
METADATA_LINE_TWO = "path: /demo_files/logs/2023/2023-11-20.md"
METADATA_LINE_THREE = "created: 2023-11-20 17:00"
METADATA_LINE_FOUR = "id: ddacf775-8d8d-4399-8535-ffe6b7864bb7"
METADATA_LINE_FIVE = "---"


@pytest.fixture
def metadata_raw() -> str:
    return "\n".join(
        [
            METADATA_LINE_ZERO,
            METADATA_LINE_ONE,
            METADATA_LINE_TWO,
            METADATA_LINE_THREE,
            METADATA_LINE_FOUR,
            METADATA_LINE_FIVE,
        ]
    )


@pytest.fixture
def metadata_section_as_list() -> list[str]:
    return [
        METADATA_LINE_ZERO,
        METADATA_LINE_ONE,
        METADATA_LINE_TWO,
        METADATA_LINE_THREE,
        METADATA_LINE_FOUR,
        METADATA_LINE_FIVE,
    ]


@pytest.fixture
def metadata_only_as_list() -> list[str]:
    return [
        METADATA_LINE_ONE,
        METADATA_LINE_TWO,
        METADATA_LINE_THREE,
        METADATA_LINE_FOUR,
    ]


@pytest.fixture
def metadata_parsed(metadata_only_as_list: list[str]) -> dict[str, str]:
    res = {}

    for line in metadata_only_as_list:
        l = re.split(r":", line, 1)
        key = l[0].strip()
        val = l[1].strip()

        res[key] = val

    return res


# HEADER

HEADER_CONTENT = "Monday, 11-12-2023"
HEADER_LINE_ZERO = "# " + HEADER_CONTENT


@pytest.fixture
def header_raw() -> str:
    return HEADER_LINE_ZERO


@pytest.fixture
def header_parsed() -> str:
    return HEADER_CONTENT


# TASKS

TASKS_LINE_ZERO = "# tasks"
TASKS_LINE_ONE = "\n"
TASKS_LINE_TWO = "## work"
TASKS_LINE_THREE = "\n"
TASKS_LINE_FOUR = (
    "- [ ] [finish_project_one](/demo_files/tasks/work/finish_project_one.md)  "
)
TASKS_LINE_FIVE = (
    "- [ ] [performance_review](/demo_files/tasks/work/performance_review.md)  "
)
TASKS_LINE_SIX = "- [ ] [scope_half_two](/demo_files/tasks/work/scope_half_two.md)  "
TASKS_LINE_SEVEN = "\n"
TASKS_LINE_EIGHT = "## personal"
TASKS_LINE_NINE = "\n"
TASKS_LINE_TEN = "- [ ] [complete_move](/demo_files/tasks/personal/complete_move.md)  "
TASKS_LINE_ELEVEN = (
    "- [ ] [create_cookbook](/demo_files/tasks/personal/create_cookbook.md)  "
)
TASKS_LINE_TWELVE = "- [ ] [personal_website_home_page](/demo_files/tasks/personal/personal_website_home_page.md)  "
TASKS_LINE_THIRTEEN = "\n"


@pytest.fixture
def tasks_raw() -> str:
    return "\n".join(
        [
            TASKS_LINE_ZERO,
            TASKS_LINE_ONE,
            TASKS_LINE_TWO,
            TASKS_LINE_THREE,
            TASKS_LINE_FOUR,
            TASKS_LINE_FIVE,
            TASKS_LINE_SIX,
            TASKS_LINE_SEVEN,
            TASKS_LINE_EIGHT,
            TASKS_LINE_NINE,
            TASKS_LINE_TEN,
            TASKS_LINE_ELEVEN,
            TASKS_LINE_TWELVE,
            TASKS_LINE_THIRTEEN,
        ]
    )


@pytest.fixture
def tasks_only_as_list() -> list[str]:
    return [
        TASKS_LINE_ONE,
        TASKS_LINE_TWO,
        TASKS_LINE_THREE,
        TASKS_LINE_FOUR,
        TASKS_LINE_FIVE,
        TASKS_LINE_SIX,
        TASKS_LINE_SEVEN,
        TASKS_LINE_EIGHT,
        TASKS_LINE_NINE,
        TASKS_LINE_TEN,
        TASKS_LINE_ELEVEN,
        TASKS_LINE_TWELVE,
        TASKS_LINE_THIRTEEN,
    ]


@pytest.fixture
def tasks_section_as_list() -> list[str]:
    return [
        TASKS_LINE_ZERO,
        TASKS_LINE_ONE,
        TASKS_LINE_TWO,
        TASKS_LINE_THREE,
        TASKS_LINE_FOUR,
        TASKS_LINE_FIVE,
        TASKS_LINE_SIX,
        TASKS_LINE_SEVEN,
        TASKS_LINE_EIGHT,
        TASKS_LINE_NINE,
        TASKS_LINE_TEN,
        TASKS_LINE_ELEVEN,
        TASKS_LINE_TWELVE,
        TASKS_LINE_THIRTEEN,
    ]


@pytest.fixture
def tasks_parsed() -> dict[str, list[tuple[TaskDBEntity, bool]]]:
    return {
        "work": [
            (
                TaskDBEntity(
                    get_first_md_link_path(TASKS_LINE_FOUR) or "/bad/path",
                ),
                not is_incomplete_md_todo_item(TASKS_LINE_FOUR),
            ),
            (
                TaskDBEntity(
                    get_first_md_link_path(TASKS_LINE_FIVE) or "/bad/path",
                ),
                not is_incomplete_md_todo_item(TASKS_LINE_FIVE),
            ),
            (
                TaskDBEntity(
                    get_first_md_link_path(TASKS_LINE_SIX) or "/bad/path",
                ),
                not is_incomplete_md_todo_item(TASKS_LINE_SIX),
            ),
        ],
        "personal": [
            (
                TaskDBEntity(get_first_md_link_path(TASKS_LINE_TEN) or "/bad/path"),
                not is_incomplete_md_todo_item(TASKS_LINE_TEN),
            ),
            (
                TaskDBEntity(
                    get_first_md_link_path(TASKS_LINE_ELEVEN) or "/bad/path",
                ),
                not is_incomplete_md_todo_item(TASKS_LINE_ELEVEN),
            ),
            (
                TaskDBEntity(
                    get_first_md_link_path(TASKS_LINE_TWELVE) or "/bad/path",
                ),
                not is_incomplete_md_todo_item(TASKS_LINE_TWELVE),
            ),
        ],
    }


# TODOS

TODOS_LINE_ZERO = "# todos"
TODOS_LINE_ONE = "\n"
TODOS_LINE_TWO = "## work"
TODOS_LINE_THREE = "\n"
TODOS_LINE_FOUR = "- [ ] email boss  "
TODOS_LINE_FIVE = "- [ ] prep for meeting  "
TODOS_LINE_SIX = "- [ ] update task status  "
TODOS_LINE_SEVEN = "\n"
TODOS_LINE_EIGHT = "## personal"
TODOS_LINE_NINE = "\n"
TODOS_LINE_TEN = "- [ ] shopping  "
TODOS_LINE_ELEVEN = "- [ ] workout  "
TODOS_LINE_TWELVE = "- [ ] write thank you notes  "
TODOS_LINE_THIRTEEN = "\n"


@pytest.fixture
def todos_raw() -> str:
    return "\n".join(
        [
            TODOS_LINE_ZERO,
            TODOS_LINE_ONE,
            TODOS_LINE_TWO,
            TODOS_LINE_THREE,
            TODOS_LINE_FOUR,
            TODOS_LINE_FIVE,
            TODOS_LINE_SIX,
            TODOS_LINE_SEVEN,
            TODOS_LINE_EIGHT,
            TODOS_LINE_NINE,
            TODOS_LINE_TEN,
            TODOS_LINE_ELEVEN,
            TODOS_LINE_TWELVE,
            TODOS_LINE_THIRTEEN,
        ]
    )


@pytest.fixture
def todos_only_as_list() -> list[str]:
    return [
        TODOS_LINE_ONE,
        TODOS_LINE_TWO,
        TODOS_LINE_THREE,
        TODOS_LINE_FOUR,
        TODOS_LINE_FIVE,
        TODOS_LINE_SIX,
        TODOS_LINE_SEVEN,
        TODOS_LINE_EIGHT,
        TODOS_LINE_NINE,
        TODOS_LINE_TEN,
        TODOS_LINE_ELEVEN,
        TODOS_LINE_TWELVE,
        TODOS_LINE_THIRTEEN,
    ]


@pytest.fixture
def todos_section_as_list() -> list[str]:
    return [
        TODOS_LINE_ZERO,
        TODOS_LINE_ONE,
        TODOS_LINE_TWO,
        TODOS_LINE_THREE,
        TODOS_LINE_FOUR,
        TODOS_LINE_FIVE,
        TODOS_LINE_SIX,
        TODOS_LINE_SEVEN,
        TODOS_LINE_EIGHT,
        TODOS_LINE_NINE,
        TODOS_LINE_TEN,
        TODOS_LINE_ELEVEN,
        TODOS_LINE_TWELVE,
        TODOS_LINE_THIRTEEN,
    ]


@pytest.fixture
def todos_parsed() -> dict[str, list[tuple[str, bool]]]:
    return {
        "work": [
            (
                strip_md_todo_item(TODOS_LINE_FOUR),
                is_incomplete_md_todo_item(TODOS_LINE_FOUR),
            ),
            (
                strip_md_todo_item(TODOS_LINE_FIVE),
                is_incomplete_md_todo_item(TODOS_LINE_FIVE),
            ),
            (
                strip_md_todo_item(TODOS_LINE_SIX),
                is_incomplete_md_todo_item(TODOS_LINE_SIX),
            ),
        ],
        "personal": [
            (
                strip_md_todo_item(TODOS_LINE_TEN),
                is_incomplete_md_todo_item(TODOS_LINE_TEN),
            ),
            (
                strip_md_todo_item(TODOS_LINE_ELEVEN),
                is_incomplete_md_todo_item(TODOS_LINE_ELEVEN),
            ),
            (
                strip_md_todo_item(TODOS_LINE_TWELVE),
                is_incomplete_md_todo_item(TODOS_LINE_TWELVE),
            ),
        ],
    }


# SUMMARY

SUMMARY_LINE_ZERO = "# summary"
SUMMARY_LINE_ONE = "\n"
SUMMARY_LINE_TWO = "## notes"
SUMMARY_LINE_THREE = "\n"
SUMMARY_LINE_FOUR = "Cameron will be out next Tuesday. Leetcode problems involving knapsacks are interesting & I should look into them more."
SUMMARY_LINE_FIVE = "\n"
SUMMARY_LINE_SIX = "## today"
SUMMARY_LINE_SEVEN = "Wrote some code, met with Ryan, and went to the store."
SUMMARY_LINE_EIGHT = "\n"
SUMMARY_LINE_NINE = "## yesterday"
SUMMARY_LINE_TEN = "\n"
SUMMARY_LINE_ELEVEN = (
    "Worked on interview prep, wrote the UI for auto-labeling, and went to the gym."
)


@pytest.fixture
def summary_raw() -> str:
    return "\n".join(
        [
            SUMMARY_LINE_ZERO,
            SUMMARY_LINE_ONE,
            SUMMARY_LINE_TWO,
            SUMMARY_LINE_THREE,
            SUMMARY_LINE_FOUR,
            SUMMARY_LINE_FIVE,
            SUMMARY_LINE_SIX,
            SUMMARY_LINE_SEVEN,
            SUMMARY_LINE_EIGHT,
            SUMMARY_LINE_NINE,
            SUMMARY_LINE_TEN,
            SUMMARY_LINE_ELEVEN,
        ]
    )


@pytest.fixture
def summary_as_list() -> list[str]:
    return [
        SUMMARY_LINE_ZERO,
        SUMMARY_LINE_ONE,
        SUMMARY_LINE_TWO,
        SUMMARY_LINE_THREE,
        SUMMARY_LINE_FOUR,
        SUMMARY_LINE_FIVE,
        SUMMARY_LINE_SIX,
        SUMMARY_LINE_SEVEN,
        SUMMARY_LINE_EIGHT,
        SUMMARY_LINE_NINE,
        SUMMARY_LINE_TEN,
        SUMMARY_LINE_ELEVEN,
    ]


@pytest.fixture
def summary_parsed() -> dict[str, str]:
    return {
        "notes": SUMMARY_LINE_FOUR,
        "today_summary": SUMMARY_LINE_SEVEN,
        "yesterday_summary": SUMMARY_LINE_ELEVEN,
    }


# whole daylog


@pytest.fixture
def daylog_raw(
    metadata_raw: str, header_raw: str, tasks_raw: str, todos_raw: str, summary_raw: str
) -> str:
    return "\n".join(
        [
            metadata_raw,
            header_raw,
            tasks_raw,
            todos_raw,
            summary_raw,
        ]
    )


@pytest.fixture
def daylog_as_list(
    metadata_section_as_list: list[str],
    header_raw: str,
    tasks_section_as_list: list[str],
    todos_section_as_list: list[str],
    summary_as_list: list[str],
) -> list[str]:
    return [
        *metadata_section_as_list,
        header_raw,
        *tasks_section_as_list,
        *todos_section_as_list,
        "# summary",
        *summary_as_list,
    ]


@pytest.fixture
def daylog_parsed(
    metadata_parsed: dict[str, str],
    header_parsed: str,
    summary_parsed: dict[str, str],
    tasks_parsed: dict[str, list[tuple[TaskDBEntity, bool]]],
    todos_parsed: dict[str, list[tuple[str, bool]]],
) -> DaylogEntityData:
    metadata = metadata_parsed
    summary = summary_parsed

    return DaylogEntityData(
        title=metadata["title"],
        path=metadata["path"],
        created=metadata["created"],
        id=metadata["id"],
        header=header_parsed,
        tasks=tasks_parsed,
        todos=todos_parsed,
        notes=summary["notes"],
        today_summary=summary["today_summary"],
        yesterday_summary=summary["yesterday_summary"],
    )


############
# TESTS
############


def test_parse_metadata_section(
    metadata_only_as_list: list[str], metadata_parsed: dict[str, str]
) -> None:
    assert _parse_metadata_section(metadata_only_as_list) == metadata_parsed


def test_parse_tasks_section(
    tasks_only_as_list: list[str],
    tasks_parsed: dict[str, list[tuple[TaskDBEntity, bool]]],
) -> None:
    assert _parse_tasks_section(tasks_only_as_list) == tasks_parsed


def test_parse_todos_section(
    todos_only_as_list: list[str], todos_parsed: dict[str, list[tuple[str, bool]]]
) -> None:
    assert _parse_todos_section(todos_only_as_list) == todos_parsed


def test_parse_summary_section(
    summary_as_list: list[str], summary_parsed: dict[str, str]
) -> None:
    assert _parse_summary_section(summary_as_list) == summary_parsed


def test_parse_entire_daylog(
    daylog_as_list: list[str], daylog_parsed: DaylogEntityData
) -> None:
    parser = DaylogDBEntityTaskFirstDataParser()
    parsed = parser.parse(daylog_as_list)
    sample = daylog_parsed

    assert parsed.title == sample.title
    assert parsed.path == sample.path
    assert parsed.created == sample.created
    assert parsed.id == sample.id

    assert len(parsed.tasks) == len(sample.tasks)

    for key in parsed.tasks:
        assert parsed.tasks[key] == sample.tasks[key]

    assert len(parsed.todos) == len(sample.todos)

    for one, two in zip(parsed.todos, sample.todos):
        assert one == two

    assert parsed.notes == sample.notes
    assert parsed.today_summary == sample.today_summary
    assert parsed.yesterday_summary == sample.yesterday_summary
