import os, datetime, uuid, dotenv

if __name__ == "__main__":
    import sys

    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])
# if not running as a script, the parent directory should already be added to path

import mndmngr.gsd.task.db_driver.driver as task_dbdriver
import mndmngr.gsd.task.utils.sort_tasks as task_sort_util


from mndmngr.config.config_parser import ConfigParser
from mndmngr.gsd.todo.todo_retrieval import get_todos_by_section


def write_header(f_name: str, date: datetime.datetime) -> None:
    with open(f_name, "w+") as f_io:
        if f_io.read() != "":
            print("file is not empty, header should be the first thing written")
            return

        f_io.write("---\n")
        f_io.write("title: " + today + "\n")
        f_io.write(
            "path: "
            + os.environ["DAILY_LOG_REL_PATH"]
            + "/"
            + str(date.year)
            + "/"
            + today_log_name
            + "\n"
        )
        f_io.write("created: " + str(date.date()) + " " + str(date.time())[:5] + "\n")
        f_io.write("id: " + str(uuid.uuid4()) + "\n")
        f_io.write("---\n\n")
        f_io.write("# " + get_weekday(date) + ", " + str(date.date()) + "\n\n")


def write_tasks(f_name: str) -> None:
    tasks = task_dbdriver.read().query_all_tasks_by_section()
    tasks = task_sort_util.get_sorted_tasks_by_section(tasks)

    if not tasks:
        print("no tasks found, skipping...")
        return None

    with open(f_name, "a+") as f_io:
        f_io.write("# tasks\n\n")

        for section in tasks:
            f_io.write("## " + section + "\n\n")
            for task in tasks[section]:
                f_io.write(
                    "-[ ] ["
                    + task.metadata.title
                    + "](/"
                    + task.metadata.path
                    + ")  \n"
                )
            f_io.write("\n")

    return None


def write_todos(f_name: str) -> None:
    todos = get_todos_by_section()

    if not todos:
        print("no todos found, skipping...")
        return None

    with open(f_name, "a+") as f_io:
        f_io.write("# todos\n\n")

        for section in todos:
            f_io.write("## " + section + "\n\n")
            f_io.write("---existing-------------\n\n")
            for todo in todos[section]:
                f_io.write("-[ ] " + todo + "  \n")
            f_io.write("\n---new today-------------\n\n")
            f_io.write("-[ ] \n")
            f_io.write("\n")

    return None


def get_weekday(date: datetime.datetime) -> str:
    today = date.weekday()

    if today == 0:
        return "Monday"
    elif today == 1:
        return "Tuesday"
    elif today == 2:
        return "Wednesday"
    elif today == 3:
        return "Thursday"
    elif today == 4:
        return "Friday"
    elif today == 5:
        return "Saturday"
    else:
        return "Sunday"


def nav_to_year(date: datetime.datetime) -> int:
    """returns the current year & navigates to the year's directory in the daily log"""
    os.chdir(os.environ["DAILY_LOG_PATH"])
    year = date.year

    if not os.path.isdir(str(year)):
        os.mkdir(str(year))

    os.chdir(str(year))
    return year


def get_yesterday_f_name(year: int) -> str | None:
    if len(os.listdir()) > 0:
        return max(os.listdir())

    # check last year for a note if there's not one this year
    os.chdir("..")
    previous_year_dir = str(year - 1)

    if not os.path.isdir(previous_year_dir):
        os.chdir(str(year))
        return None

    os.chdir(previous_year_dir)

    if len(os.listdir()) == 0:
        return None

    yesterday = max(os.listdir())

    os.chdir("..")
    os.chdir(str(year))

    return yesterday


def get_yesterday_summary(year: int) -> str | None:
    yesterday = get_yesterday_f_name(year)

    if yesterday == None:
        # no summary for yesterday
        return None

    # get yesterday's summary
    return ""


# START OF SCRIPT

cp = ConfigParser()
config = cp.get_config()

if not config:
    print("config is empty")
    exit(1)

date = datetime.datetime.now()
year = nav_to_year(date)

# handle yesterday: update tasks, todos as required by presence of checkmarks

yesterday_summary = get_yesterday_summary(year)

today = str(date.date())
today_log_name = today + ".md"

# for now, overwrite (i.e. leave following commented out)

# if (os.path.isfile(today_log_name)):
#   print("you've already created a daily log for today")
#   exit(1)

write_header(today_log_name, date)
write_tasks(today_log_name)
write_todos(today_log_name)
# write_today_summary
# write_yesterday_summary
