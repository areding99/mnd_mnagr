#!/usr/bin/env python3

import os, datetime, uuid, dotenv, sys

dotenv.load_dotenv()
sys.path.append(os.environ["MND_MNGR_ROOT"])

from mndmngr.gsd.data.entities.Daylog.DaylogDBEntity import DaylogDBEntity
from mndmngr.gsd.data.entities.Daylog.DaylogDBEntityWriter import DaylogDBEntityWriter
from mndmngr.gsd.data.entities.Daylog.DaylogDBEntityTaskFirstDataParser import (
    DaylogDBEntityTaskFirstDataParser,
)
from mndmngr.gsd.data.entities.Daylog.DaylogEntityData import DaylogEntityData
from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity
from mndmngr.gsd.data.entities.Task.convenience.get_open_tasks_by_section import (
    get_open_tasks_by_section,
)
from mndmngr.gsd.data.entities.Task.convenience.set_task_status import set_task_status
from mndmngr.gsd.data.entities.Task.convenience.sort_tasks import sort_tasks
from mndmngr.gsd.data.queries.PathDBQuery import PathDBQuery
from mndmngr.gsd.utilities.get_weekday import get_weekday

import mndmngr.gsd.data.EntityManager as EntityManager


def create_year_if_not_exists(year: int) -> None:
    if not os.path.exists(
        os.environ["USER_ROOT"] + os.environ["DAILY_LOG_REL_PATH"] + "/" + str(year)
    ):
        os.mkdir(
            os.environ["USER_ROOT"] + os.environ["DAILY_LOG_REL_PATH"] + "/" + str(year)
        )


def get_yesterday_f_name(year: int) -> str | None:
    # check this year for yesterday's log
    curr_year_dir = (
        os.environ["USER_ROOT"] + os.environ["DAILY_LOG_REL_PATH"] + "/" + str(year)
    )

    if not os.path.exists(curr_year_dir):
        raise ValueError("current year directory should exist")

    curr_year_dir_contents = os.listdir(curr_year_dir)

    if len(curr_year_dir_contents) != 0:
        return (
            os.environ["USER_ROOT"]
            + os.environ["DAILY_LOG_REL_PATH"]
            + "/"
            + str(year)
            + "/"
            + max(curr_year_dir_contents)
        )

    # check last year for a note if there's not one this year
    prev_year_dir = (
        os.environ["USER_ROOT"] + os.environ["DAILY_LOG_REL_PATH"] + "/" + str(year - 1)
    )

    if not os.path.exists(prev_year_dir):
        return None

    prev_year_dir_contents = os.listdir(prev_year_dir)

    if len(prev_year_dir_contents) != 0:
        return (
            os.environ["USER_ROOT"]
            + os.environ["DAILY_LOG_REL_PATH"]
            + "/"
            + str(year - 1)
            + "/"
            + max(prev_year_dir_contents)
        )

    return None


def get_yesterday(year: int) -> DaylogDBEntity | None:
    yesterday = get_yesterday_f_name(year)

    if yesterday is None:
        return None

    query = PathDBQuery()
    query.set_query_args(yesterday)

    return EntityManager.get(DaylogDBEntity, DaylogDBEntityTaskFirstDataParser(), query)


def today_exists(path: str) -> bool:
    if os.path.exists(path):
        return True

    return False


def get_sorted_formatted_tasks_by_section() -> (
    dict[str, list[tuple[TaskDBEntity, bool]]]
):
    open_tasks_by_section = get_open_tasks_by_section()
    sorted_formatted_tasks_by_section: dict[str, list[tuple[TaskDBEntity, bool]]] = {}

    for section in open_tasks_by_section:
        sorted_formatted_tasks_by_section[section] = [
            (task, False)
            for task in sort_tasks(open_tasks_by_section[section])
            if task is not None
        ]

    return sorted_formatted_tasks_by_section


def collate_and_write_daylog(
    title: str,
    path: str,
    created: str,
    id: str,
    header: str,
    tasks: dict[str, list[tuple[TaskDBEntity, bool]]],
    todos: dict[str, list[tuple[str, bool]]],
    notes: str,
    today_summary: str,
    yesterday_summary: str,
) -> None:
    daylog_data = DaylogEntityData(
        title,
        path,
        created,
        id,
        header,
        tasks,
        todos,
        notes,
        today_summary,
        yesterday_summary,
    )
    daylog = DaylogDBEntity(path, daylog_data)
    EntityManager.write(daylog, DaylogDBEntityWriter())


def create_daylog() -> None:
    date = datetime.datetime.now()
    year = date.year

    # TODO seems to be a bug somewhere that doesn't handle the previous year

    # create metadata as necessary
    today = str(date.date())
    rel_path = (
        DaylogDBEntity.get_entity_path_rel() + "/" + str(year) + "/" + today + ".md"
    )
    created = str(date.date()) + " " + str(date.time())[:5]
    id = str(uuid.uuid4())
    header = get_weekday(date) + ", " + str(date.date())

    if today_exists(DaylogDBEntity.get_entity_path_prefix() + rel_path):
        print("today's daylog already exists")
        return

    create_year_if_not_exists(year)
    yesterday = get_yesterday(year)

    if yesterday is None or not yesterday.is_initialized():
        collate_and_write_daylog(
            today,
            rel_path,
            created,
            id,
            header,
            get_sorted_formatted_tasks_by_section(),
            {},
            "",
            "",
            "",
        )

        return None

    yesterday_data = yesterday.get_data()

    if yesterday_data is None:
        raise ValueError("data cannot be None if entity is initialized")

    # handle updates from yesterday

    for section in yesterday_data.tasks:
        for task, is_complete in yesterday_data.tasks[section]:
            if is_complete:
                set_task_status(task, "closed")

    # collect data to carry over to today

    open_todos_by_section: dict[str, list[str]] = {}

    for section in yesterday_data.todos:
        for todo, is_complete in yesterday_data.todos[section]:
            if not is_complete:
                if section not in open_todos_by_section:
                    open_todos_by_section[section] = []

                open_todos_by_section[section].append(todo)

    formatted_todos_by_section: dict[str, list[tuple[str, bool]]] = {}

    for section in open_todos_by_section:
        formatted_todos_by_section[section] = [
            (todo, False) for todo in open_todos_by_section[section]
        ]

    yesterday_summary = yesterday_data.today_summary

    collate_and_write_daylog(
        today,
        rel_path,
        created,
        id,
        header,
        get_sorted_formatted_tasks_by_section(),
        formatted_todos_by_section,
        "",
        "",
        yesterday_summary,
    )


# run it!
create_daylog()
