import os, dotenv

if __name__ == "__main__":
    import sys

    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])
# if not running as a script, the parent directory should already be added to path


def get_todos_by_section() -> dict[str, list[str]] | None:
    # TODO implement
    # retrieve from yesterday
    # just copy whatever headers existed yesterday rather than impose some config

    return {"work": ["sample 1", "sample 2"], "personal": ["sample3", "sample4"]}


# at the end of the day, finished todos can be closed & opened todos can be added
