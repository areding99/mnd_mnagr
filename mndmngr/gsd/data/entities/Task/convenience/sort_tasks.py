import os, sys, dotenv

if __name__ == "__main__":
    dotenv.load_dotenv()
    sys.path.append(os.environ["MND_MNGR_ROOT"])

from mndmngr.config.GSDConfigParser import GSDConfigParser, GSDConfig
from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity
from mndmngr.gsd.data.entities.Task.TaskEntityData import TaskEntityData


def sort_tasks(tasks: list[TaskDBEntity]) -> list[TaskDBEntity]:
    config: GSDConfig | None = GSDConfigParser().get_config()

    if not config:
        # TODO: move exception to GSDConfigParser
        raise ValueError("config is None")

    category_sort_order = config.tasks.task_sort_order

    attr_sort_order: dict[str, list[str]] = {}

    for category in category_sort_order:
        if hasattr(config.tasks.task_config, category):
            attr_sort_order[category] = getattr(config.tasks.task_config, category)
        else:
            # category defines no sort order over an enum of attributes, i.e. date
            attr_sort_order[category] = []

    return _sort_tasks_impl(tasks, category_sort_order, attr_sort_order, 0)


def _sort_tasks_impl(
    tasks: list[TaskDBEntity],
    categories: list[str],
    attr_sort_order: dict[str, list[str]],
    category_idx: int,
) -> list[TaskDBEntity]:
    """Recursively bucket sort tasks according sort order by attribute."""
    if len(tasks) <= 1 or category_idx >= len(categories):
        return tasks

    category: str = categories[category_idx]

    attrs = []
    if category in attr_sort_order:
        attrs = attr_sort_order[category]

    attr_groups: dict[str, list[TaskDBEntity]] = {}
    undefined_attrs: list[str] = []

    # bucket by attribute val
    for task in tasks:
        if not task.is_initialized():
            raise ValueError("task is not initialized")

        data = task.get_data()
        if data is None:
            raise ValueError("data cannot be None if task is initialized")

        attr_val = getattr(data, category)
        if attr_val in attr_groups:
            attr_groups[attr_val].append(task)
        else:
            attr_groups[attr_val] = [task]
            if attr_val not in attrs:
                undefined_attrs.append(attr_val)

    sorted_tasks: list[TaskDBEntity] = []

    for attr in attrs:
        if attr not in attr_groups:
            continue
        for task in _sort_tasks_impl(
            attr_groups[attr], categories, attr_sort_order, category_idx + 1
        ):
            sorted_tasks.append(task)

    if len(undefined_attrs) > 0:
        undefined_attrs.sort()

        for attr in undefined_attrs:
            for task in _sort_tasks_impl(
                attr_groups[attr], categories, attr_sort_order, category_idx + 1
            ):
                sorted_tasks.append(task)

    return sorted_tasks
