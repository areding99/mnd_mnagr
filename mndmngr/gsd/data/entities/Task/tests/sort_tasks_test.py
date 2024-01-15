import pytest
import sys, dotenv, os

dotenv.load_dotenv()
sys.path.append(os.environ["PROJECT_ROOT"])

from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity
from mndmngr.gsd.data.entities.Task.TaskEntityData import TaskEntityData
from mndmngr.gsd.data.entities.Task.convenience.sort_tasks import _sort_tasks_impl

############
# SETUP
############


@pytest.fixture
def tasks() -> list[TaskDBEntity]:
    task_data_1 = TaskEntityData(
        title="task 1",
        path="path/to/task/1",
        created="2021-01-01",
        id="1234",
        requestor="me",
        subscribers=["me"],
        status="backlog",
        urgency="low",
        tags=["chore"],
        priority="high",
        due="2021-01-01",
        body=["task 1 body"],
    )

    task_one = TaskDBEntity("path/to/task/1", task_data_1)

    task_data_2 = TaskEntityData(
        title="task 2",
        path="path/to/task/2",
        created="2021-01-01",
        id="1234",
        requestor="me",
        subscribers=["me"],
        status="planned",
        urgency="low",
        tags=["chore"],
        priority="medium",
        due="2021-01-01",
        body=["task 2 body"],
    )

    task_two = TaskDBEntity("path/to/task/2", task_data_2)

    task_data_3 = TaskEntityData(
        title="task 3",
        path="path/to/task/3",
        created="2021-01-01",
        id="1234",
        requestor="me",
        subscribers=["me"],
        status="in_progress",
        urgency="low",
        tags=["chore"],
        priority="low",
        due="2021-01-01",
        body=["task 3 body"],
    )

    task_three = TaskDBEntity("path/to/task/3", task_data_3)

    task_data_4 = TaskEntityData(
        title="task 4",
        path="path/to/task/4",
        created="2021-01-01",
        id="1234",
        requestor="me",
        subscribers=["me"],
        status="in_progress",
        urgency="medium",
        tags=["chore"],
        priority="low",
        due="2021-01-01",
        body=["task 4 body"],
    )

    task_four = TaskDBEntity("path/to/task/4", task_data_4)

    task_data_5 = TaskEntityData(
        title="task 5",
        path="path/to/task/5",
        created="2021-01-01",
        id="1234",
        requestor="me",
        subscribers=["me"],
        status="in_progress",
        urgency="high",
        tags=["chore"],
        priority="low",
        due="2021-01-01",
        body=["task 5 body"],
    )

    task_five = TaskDBEntity("path/to/task/5", task_data_5)

    task_data_6 = TaskEntityData(
        title="task 6",
        path="path/to/task/6",
        created="2021-01-01",
        id="1234",
        requestor="me",
        subscribers=["me"],
        status="in_progress",
        urgency="medium",
        tags=["chore"],
        priority="low",
        due="2021-01-01",
        body=["task 6 body"],
    )

    task_six = TaskDBEntity("path/to/task/6", task_data_6)

    task_data_7 = TaskEntityData(
        title="task 7",
        path="path/to/task/7",
        created="2021-01-01",
        id="1234",
        requestor="me",
        subscribers=["me"],
        status="in_progress",
        urgency="low",
        tags=["chore"],
        priority="high",
        due="2021-01-01",
        body=["task 7 body"],
    )

    task_seven = TaskDBEntity("path/to/task/7", task_data_7)

    task_data_8 = TaskEntityData(
        title="task 8",
        path="path/to/task/8",
        created="2020-01-01",
        id="1234",
        requestor="me",
        subscribers=["me"],
        status="in_progress",
        urgency="low",
        tags=["chore"],
        priority="high",
        due="2022-01-01",
        body=["task 8 body"],
    )

    task_eight = TaskDBEntity("path/to/task/8", task_data_8)

    task_data_9 = TaskEntityData(
        title="task 9",
        path="path/to/task/9",
        created="2021-04-01",
        id="1234",
        requestor="me",
        subscribers=["me"],
        status="in_progress",
        urgency="low",
        tags=["chore"],
        priority="medium",
        due="2022-01-13",
        body=["task 9 body"],
    )

    task_nine = TaskDBEntity("path/to/task/9", task_data_9)

    task_data_10 = TaskEntityData(
        title="task 10",
        path="path/to/task/10",
        created="2021-01-29",
        id="1234",
        requestor="me",
        subscribers=["me"],
        status="in_progress",
        urgency="low",
        tags=["chore"],
        priority="low",
        due="2021-04-01",
        body=["task 10 body"],
    )

    task_ten = TaskDBEntity("path/to/task/10", task_data_10)

    return [
        task_one,
        task_two,
        task_three,
        task_four,
        task_five,
        task_six,
        task_seven,
        task_eight,
        task_nine,
        task_ten,
    ]


@pytest.fixture
def tasks_expected_order_one(
    tasks: list[TaskDBEntity],
) -> tuple[list[str], dict[str, list[str]], list[TaskDBEntity]]:
    task_sort_order = [
        "status",
        "urgency",
        "priority",
        "due",
    ]

    attr_sort_order = {
        "status": ["backlog", "planned", "in_progress", "closed"],
        "priority": ["high", "medium", "low"],
        "urgency": ["high", "medium", "low"],
    }

    tasks = [
        tasks[
            0
        ],  # task 1, status: backlog, urgency: low, priority: high, due: 2021-01-01
        tasks[
            1
        ],  # task 2, status: planned, urgency: low, priority: medium, due: 2021-01-01
        tasks[
            4
        ],  # task 5, status: in_progress, urgency: high, priority: low, due: 2021-01-01
        tasks[
            3
        ],  # task 4, status: in_progress, urgency: medium, priority: low, due: 2021-01-01
        tasks[
            5
        ],  # task 6, status: in_progress, urgency: medium, priority: low, due: 2021-01-01
        tasks[
            6
        ],  # task 7, status: in_progress, urgency: low, priority: high, due: 2021-01-01
        tasks[
            7
        ],  # task 8, status: in_progress, urgency: low, priority: high, due: 2022-01-01
        tasks[
            8
        ],  # task 9, status: in_progress, urgency: low, priority: medium, due: 2022-01-13
        tasks[
            2
        ],  # task 3, status: in_progress, urgency: low, priority: low, due: 2021-01-01
        tasks[
            9
        ],  # task 10, status: in_progress, urgency: low, priority: low, due: 2021-04-01
    ]

    return (task_sort_order, attr_sort_order, tasks)


@pytest.fixture
def tasks_expected_order_two(
    tasks: list[TaskDBEntity],
) -> tuple[list[str], dict[str, list[str]], list[TaskDBEntity]]:
    task_sort_order = [
        "due",
        "status",
    ]

    attr_sort_order = {
        "status": ["backlog", "planned", "in_progress", "closed"],
        "priority": ["high", "medium", "low"],
        "urgency": ["high", "medium", "low"],
    }

    tasks = [
        tasks[
            0
        ],  # task 1, status: backlog, urgency: low, priority: high, due: 2021-01-01
        tasks[
            1
        ],  # task 2, status: planned, urgency: low, priority: medium, due: 2021-01-01
        tasks[
            2
        ],  # task 3, status: in_progress, urgency: low, priority: low, due: 2021-01-01
        tasks[
            3
        ],  # task 4, status: in_progress, urgency: medium, priority: low, due: 2021-01-01
        tasks[
            4
        ],  # task 5, status: in_progress, urgency: high, priority: low, due: 2021-01-01
        tasks[
            5
        ],  # task 6, status: in_progress, urgency: medium, priority: low, due: 2021-01-01
        tasks[
            6
        ],  # task 7, status: in_progress, urgency: low, priority: high, due: 2021-01-01
        tasks[
            9
        ],  # task 10, status: in_progress, urgency: low, priority: low, due: 2021-04-01
        tasks[
            7
        ],  # task 8, status: in_progress, urgency: low, priority: high, due: 2022-01-01
        tasks[
            8
        ],  # task 9, status: in_progress, urgency: low, priority: medium, due: 2022-01-13
    ]

    return (task_sort_order, attr_sort_order, tasks)


@pytest.fixture
def tasks_expected_order_three(
    tasks: list[TaskDBEntity],
) -> tuple[list[str], dict[str, list[str]], list[TaskDBEntity]]:
    task_sort_order = [
        "status",
        "priority",
        "due",
        "urgency",
    ]

    attr_sort_order = {
        "status": ["backlog", "planned", "in_progress", "closed"],
        "priority": ["high", "medium", "low"],
        "urgency": ["high", "medium", "low"],
    }

    tasks = [
        tasks[
            0
        ],  # task 1, status: backlog, urgency: low, priority: high, due: 2021-01-01
        tasks[
            1
        ],  # task 2, status: planned, urgency: low, priority: medium, due: 2021-01-01
        tasks[
            6
        ],  # task 7, status: in_progress, urgency: low, priority: high, due: 2021-01-01
        tasks[
            7
        ],  # task 8, status: in_progress, urgency: low, priority: high, due: 2022-01-01
        tasks[
            8
        ],  # task 9, status: in_progress, urgency: low, priority: medium, due: 2022-01-13
        tasks[
            4
        ],  # task 5, status: in_progress, urgency: high, priority: low, due: 2021-01-01
        tasks[
            3
        ],  # task 4, status: in_progress, urgency: medium, priority: low, due: 2021-01-01
        tasks[
            5
        ],  # task 6, status: in_progress, urgency: medium, priority: low, due: 2021-01-01
        tasks[
            2
        ],  # task 3, status: in_progress, urgency: low, priority: low, due: 2021-01-01
        tasks[
            9
        ],  # task 10, status: in_progress, urgency: low, priority: low, due: 2021-04-01
    ]

    return (task_sort_order, attr_sort_order, tasks)


############
# TESTS
############


def test_sort_order_one(
    tasks: list[TaskDBEntity],
    tasks_expected_order_one: tuple[
        list[str],
        dict[
            str,
            list[str],
        ],
        list[TaskDBEntity],
    ],
) -> None:
    (
        task_sort_order,
        attr_sort_order,
        tasks_expected_order,
    ) = tasks_expected_order_one
    sorted_tasks = _sort_tasks_impl(tasks, task_sort_order, attr_sort_order, 0)

    assert sorted_tasks == tasks_expected_order


def test_sort_order_two(
    tasks: list[TaskDBEntity],
    tasks_expected_order_two: tuple[
        list[str], dict[str, list[str]], list[TaskDBEntity]
    ],
) -> None:
    (
        task_sort_order,
        attr_sort_order,
        tasks_expected_order,
    ) = tasks_expected_order_two
    sorted_tasks = _sort_tasks_impl(tasks, task_sort_order, attr_sort_order, 0)

    assert sorted_tasks == tasks_expected_order


def test_sort_order_three(
    tasks: list[TaskDBEntity],
    tasks_expected_order_three: tuple[
        list[str], dict[str, list[str]], list[TaskDBEntity]
    ],
) -> None:
    (
        task_sort_order,
        attr_sort_order,
        tasks_expected_order,
    ) = tasks_expected_order_three
    sorted_tasks = _sort_tasks_impl(tasks, task_sort_order, attr_sort_order, 0)

    assert sorted_tasks == tasks_expected_order
