import os, dotenv

if __name__ == "__main__":
    import sys

    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])

from mndmngr.gsd.day_log.db_driver.lib.parsing import parse_day_log


def _query_raw_day_log_by_title(title: str) -> list[str] | None:
    year = title[:4]
    path = os.environ["DAILY_LOG_PATH"] + "/" + year + "/" + title

    if not os.path.exists(path):
        print("Could not find day log with title: " + title)
        return None

    with open(path, "r") as f_io:
        return f_io.readlines()


def _query_raw_day_logs_for_year(year: str) -> list[list[str]] | None:
    cwd = os.getcwd()

    try:
        os.chdir(os.environ["DAILY_LOG_PATH"] + "/" + year)
    except FileNotFoundError:
        print("No logs found for year: " + year)
        os.chdir(cwd)
        return None

    day_logs: list[list[str]] = []

    for dl_file in os.listdir():
        with open(dl_file, "r") as f_io:
            day_logs.append(f_io.readlines())

    os.chdir(cwd)
    return day_logs


def _query_raw_last_recorded_day_log_of_year(year: str) -> list[str] | None:
    cwd = os.getcwd()

    os.chdir(os.environ["DAILY_LOG_PATH"] + "/" + year)

    last_day_log = max(os.listdir())

    if not last_day_log:
        os.chdir(cwd)
        return None

    day_log: list[str] | None = None

    with open(last_day_log, "r") as f_io:
        day_log = f_io.readlines()

    os.chdir(cwd)
    return day_log


raw_dl = _query_raw_last_recorded_day_log_of_year("2023")
if raw_dl:
    parse_day_log(raw_dl)
