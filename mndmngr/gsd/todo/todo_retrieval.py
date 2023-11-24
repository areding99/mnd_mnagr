import os, dotenv

if __name__ == "__main__":
    import sys

    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])
# if not running as a script, the parent directory should already be added to path


def get_todos_by_section() -> dict[str, list[str]] | None:
    cwd = os.getcwd()

    os.chdir(os.environ["TODOS_PATH"])
    todos_by_section: dict[str, list[str]] = {}

    for file in os.listdir():
        with open(file, "r") as f_io:
            todos_by_section[file] = []
            # iterate over lines in the file
            for line in f_io.readlines():
                todos_by_section[file].append(line.strip())

    os.chdir(cwd)

    return todos_by_section


# use a todo section that will be generated from existing & is visibly separate - new todos should have their own section so that
# at the end of the day, finished todos can be closed & opened todos can be added
# if you want to update a todo, you should check it as finished in the generated section & add a new todo in the manual section
