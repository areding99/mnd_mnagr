import os, sys, dotenv


if __name__ == "__main__":
    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])

from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity
from mndmngr.gsd.data.entities.Task.TaskDBEntityDataParser import TaskDBEntityDataParser
from mndmngr.gsd.data.queries.PathDBQuery import PathDBQuery
import mndmngr.gsd.data.EntityManager as EM


def parse_task() -> None:
    pass


# probably some lib to streamline this but should consist of a text file in some various formats
# need to decide how to handle parsing an unfamiliar shape, too

path = os.environ["TASKS_PATH"] + "/personal/complete_move.md"

task = EM.get(TaskDBEntity, TaskDBEntityDataParser(), PathDBQuery(), path)

print(task.get_data().tags)
