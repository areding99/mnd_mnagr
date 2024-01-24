import re
import pytest
import sys, dotenv, os

dotenv.load_dotenv()
sys.path.append(os.environ["MND_MNGR_ROOT"])

from mndmngr.gsd.data.entities.Task.TaskEntityData import TaskEntityData
from mndmngr.gsd.data.entities.Task.TaskDBEntityDataParser import (
    TaskDBEntityDataParser,
    _parse_about_section,
    _parse_metadata_section,
)

###############
# SETUP
###############

# METADATA

METADATA_TITLE = "2023-11-20"
METADATA_PATH = "/demo_files/logs/2023/2023-11-20.md"
METADATA_CREATED = "2023-11-20 17:00"
METADATA_ID = "ddacf775-8d8d-4399-8535-ffe6b7864bb7"

METADATA_LINE_ZERO = "---"
METADATA_LINE_ONE = "title: " + METADATA_TITLE
METADATA_LINE_TWO = "path: " + METADATA_PATH
METADATA_LINE_THREE = "created: " + METADATA_CREATED
METADATA_LINE_FOUR = "id: " + METADATA_ID
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


# ABOUT

ABOUT_REQUESTOR = "andy"
ABOUT_SUBSCRIBERS = ["my_manager", "me"]
ABOUT_STATUS = "in_progress"
ABOUT_URGENCY = "high"
ABOUT_PRIORITY = "low"
ABOUT_TAGS = ["feature"]
ABOUT_DUE = "2023-11-21"


ABOUT_LINE_ZERO = "# about"
ABOUT_LINE_ONE = "\n"
ABOUT_LINE_TWO = "|             |                |"
ABOUT_LINE_THREE = "| ----------- | -------------- |"
ABOUT_LINE_FOUR = "| requestor   | " + ABOUT_REQUESTOR + "           |"
ABOUT_LINE_FIVE = (
    "| subscribers | " + ABOUT_SUBSCRIBERS[0] + ", " + ABOUT_SUBSCRIBERS[1] + " |"
)
ABOUT_LINE_SIX = "| status      | " + ABOUT_STATUS + "    |"
ABOUT_LINE_SEVEN = "| urgency     | " + ABOUT_URGENCY + "           |"
ABOUT_LINE_EIGHT = "| priority    | " + ABOUT_PRIORITY + "            |"
ABOUT_LINE_NINE = "| tags        | " + ABOUT_TAGS[0] + "        |"
ABOUT_LINE_TEN = "| due         | " + ABOUT_DUE + "     |"
ABOUT_LINE_ELEVEN = "\n"


@pytest.fixture
def about_raw() -> str:
    return "\n".join(
        [
            ABOUT_LINE_ZERO,
            ABOUT_LINE_ONE,
            ABOUT_LINE_TWO,
            ABOUT_LINE_THREE,
            ABOUT_LINE_FOUR,
            ABOUT_LINE_FIVE,
            ABOUT_LINE_SIX,
            ABOUT_LINE_SEVEN,
            ABOUT_LINE_EIGHT,
            ABOUT_LINE_NINE,
            ABOUT_LINE_TEN,
            ABOUT_LINE_ELEVEN,
        ]
    )


@pytest.fixture
def about_section_as_list() -> list[str]:
    return [
        ABOUT_LINE_ZERO,
        ABOUT_LINE_ONE,
        ABOUT_LINE_TWO,
        ABOUT_LINE_THREE,
        ABOUT_LINE_FOUR,
        ABOUT_LINE_FIVE,
        ABOUT_LINE_SIX,
        ABOUT_LINE_SEVEN,
        ABOUT_LINE_EIGHT,
        ABOUT_LINE_NINE,
        ABOUT_LINE_TEN,
        ABOUT_LINE_ELEVEN,
    ]


@pytest.fixture
def about_only_as_list() -> list[str]:
    return [
        ABOUT_LINE_FOUR,
        ABOUT_LINE_FIVE,
        ABOUT_LINE_SIX,
        ABOUT_LINE_SEVEN,
        ABOUT_LINE_EIGHT,
        ABOUT_LINE_NINE,
        ABOUT_LINE_TEN,
    ]


@pytest.fixture
def about_parsed() -> dict[str, str | list[str]]:
    res: dict[str, str | list[str]] = {}

    res["requestor"] = ABOUT_REQUESTOR
    res["subscribers"] = ABOUT_SUBSCRIBERS
    res["status"] = ABOUT_STATUS
    res["urgency"] = ABOUT_URGENCY
    res["priority"] = ABOUT_PRIORITY
    res["tags"] = ABOUT_TAGS
    res["due"] = ABOUT_DUE

    return res


# RAW BODY

OVERVIEW_LINE_ZERO = "# overview"
OVERVIEW_LINE_ONE = "\n"
OVERVIEW_LINE_TWO = "My first project with the new team! It's a small one & not too important but I promised to have it done on time."
OVERVIEW_LINE_THREE = "\n"


PROGRESS_LINE_ZERO = "# progress"
PROGRESS_LINE_ONE = "\n"
PROGRESS_LINE_TWO = "- [ ] get requirements"
PROGRESS_LINE_THREE = "- [ ] review codebase"
PROGRESS_LINE_FOUR = "- [ ] write the feature"
PROGRESS_LINE_FIVE = "- [ ] test"
PROGRESS_LINE_SIX = "- [ ] ship"
PROGRESS_LINE_SEVEN = "\n"


@pytest.fixture
def raw_body(
    metadata_section_as_list: list[str], about_section_as_list: list[str]
) -> str:
    return "\n".join(
        [
            *metadata_section_as_list,
            *about_section_as_list,
            OVERVIEW_LINE_ZERO,
            OVERVIEW_LINE_ONE,
            OVERVIEW_LINE_TWO,
            OVERVIEW_LINE_THREE,
            PROGRESS_LINE_ZERO,
            PROGRESS_LINE_ONE,
            PROGRESS_LINE_TWO,
            PROGRESS_LINE_THREE,
            PROGRESS_LINE_FOUR,
            PROGRESS_LINE_FIVE,
            PROGRESS_LINE_SIX,
            PROGRESS_LINE_SEVEN,
        ]
    )


@pytest.fixture
def body_as_list(
    metadata_section_as_list: list[str], about_section_as_list: list[str]
) -> list[str]:
    return [
        *metadata_section_as_list,
        *about_section_as_list,
        OVERVIEW_LINE_ZERO,
        OVERVIEW_LINE_ONE,
        OVERVIEW_LINE_TWO,
        OVERVIEW_LINE_THREE,
        PROGRESS_LINE_ZERO,
        PROGRESS_LINE_ONE,
        PROGRESS_LINE_TWO,
        PROGRESS_LINE_THREE,
        PROGRESS_LINE_FOUR,
        PROGRESS_LINE_FIVE,
        PROGRESS_LINE_SIX,
        PROGRESS_LINE_SEVEN,
    ]


@pytest.fixture
def body_parsed(body_as_list: list[str]) -> TaskEntityData:
    return TaskEntityData(
        title=METADATA_TITLE,
        path=METADATA_PATH,
        created=METADATA_CREATED,
        id=METADATA_ID,
        requestor=ABOUT_REQUESTOR,
        subscribers=ABOUT_SUBSCRIBERS,
        status=ABOUT_STATUS,
        urgency=ABOUT_URGENCY,
        tags=ABOUT_TAGS,
        priority=ABOUT_PRIORITY,
        due=ABOUT_DUE,
        body=body_as_list,
    )


#############
# TESTS
#############


def test_parse_metadata_section(
    metadata_only_as_list: list[str], metadata_parsed: dict[str, str]
) -> None:
    assert _parse_metadata_section(metadata_only_as_list) == metadata_parsed


def test_parse_about_section(
    about_only_as_list: list[str], about_parsed: dict[str, str | list[str]]
) -> None:
    assert _parse_about_section(about_only_as_list) == about_parsed


def test_parse_entire(
    body_as_list: list[str],
    body_parsed: TaskEntityData,
) -> None:
    parser = TaskDBEntityDataParser()
    parsed = parser.parse(body_as_list)

    assert parsed.title == body_parsed.title
    assert parsed.path == body_parsed.path
    assert parsed.created == body_parsed.created
    assert parsed.id == body_parsed.id
    assert parsed.requestor == body_parsed.requestor
    assert parsed.subscribers == body_parsed.subscribers
    assert parsed.status == body_parsed.status
    assert parsed.urgency == body_parsed.urgency
    assert parsed.tags == body_parsed.tags
    assert parsed.priority == body_parsed.priority
    assert parsed.due == body_parsed.due
    assert parsed.body == body_parsed.body
