import os, re, sys, dotenv

if __name__ == "__main__":
    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])

from mndmngr.config.config_parser import ConfigParser, Config
from mndmngr.gsd.task_and_todo.task.task import Task


def sort_tasks(tasks: list[Task]) -> list[Task] | None:
    config: Config | None = ConfigParser().get_config()

    if not config:
        return None

    category_sort_order = config.tasks.task_sort_order

    attr_sort_order: dict[str, list[str]] = {}

    for category in category_sort_order:
        if hasattr(config.tasks.task_config, category):
            attr_sort_order[category] = getattr(config.tasks.task_config, category)
        else:
            # category defines no sort order over an enum of attributes, i.e. date
            attr_sort_order[category] = []

    return _sort_tasks_impl(tasks, category_sort_order, attr_sort_order, 0)


def get_sorted_tasks_by_section(
    tasks_by_section: dict[str, list[Task]]
) -> dict[str, list[Task]] | None:
    """returns a list of tasks names, organized by section & priority"""
    sorted_tasks_by_section: dict[str, list[Task]] = {}

    for section, tasks in tasks_by_section.items():
        sorted_section = sort_tasks(tasks)

        if not sorted_section:
            continue

        sorted_tasks_by_section[section] = sorted_section

    return sorted_tasks_by_section


# TODO
# def split_tasks_by_subsection():
#   """split tasks into subsections based on attributes (i.e. tags, status, etc.)"""
#   pass


def _sort_tasks_impl(
    tasks: list[Task],
    categories: list[str],
    attr_sort_order: dict[str, list[str]],
    category_idx: int,
) -> list[Task]:
    """Recursively bucket sort tasks according sort order by attribute."""
    if len(tasks) <= 1 or category_idx >= len(categories):
        return tasks

    category: str = categories[category_idx]
    attrs = attr_sort_order[category]
    attr_groups: dict[str, list[Task]] = {}
    # TODO use attribute value here, even if not defined, so that subordering can be preserved for less important categories
    attr_groups["other"] = []

    # bucket by attribute val
    for task in tasks:
        if hasattr(task.about_section, category):
            attr_val = getattr(task.about_section, category)
            if attr_val in attrs:
                if attr_val in attr_groups:
                    attr_groups[attr_val].append(task)
                else:
                    attr_groups[attr_val] = [task]
            else:
                # the category doesn't defined attributes
                attr_groups["other"].append(task)
        else:
            # this means task has some category the config doesn't define
            raise Exception("Undefined category: " + category)

    sorted_tasks: list[Task] = []

    for val in attrs:
        if val not in attr_groups:
            continue
        for task in _sort_tasks_impl(
            attr_groups[val], categories, attr_sort_order, category_idx + 1
        ):
            sorted_tasks.append(task)
    else:
        # categories without a sort order defined on attributes (i.e. date due)
        # sort them in ascending order for now
        others = attr_groups["other"]
        others.sort(key=lambda t: getattr(t.about_section, category))

        for task in others:
            sorted_tasks.append(task)

    return sorted_tasks
