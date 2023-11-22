import os, re, sys, dotenv

if __name__ == "__main__":
  dotenv.load_dotenv()
  sys.path.append(os.environ['PROJECT_ROOT'])

from mndmngr.config.config_parser import ConfigParser, Config
from mndmngr.gsd.task_and_todo.task.sort_tasks import sort_tasks
from mndmngr.gsd.task_and_todo.task.task_retrieval_utils import retrieve_parse_all_tasks, Task

def get_sorted_tasks_by_section() -> dict[str, list[Task]] | None:
  """returns a list of tasks names, organized by section & priority"""
  config: Config | None = ConfigParser().get_config()

  tasks_by_section = retrieve_parse_all_tasks()
  sorted_tasks_by_section: dict[str, list[Task]] = {}

  for (section, tasks) in tasks_by_section.items():
    sorted_section = sort_tasks(tasks)

    if not sorted_section:
      continue

    sorted_tasks_by_section[section] = sorted_section


  print(sorted_tasks_by_section)
  return sorted_tasks_by_section

get_sorted_tasks_by_section()



# TODO
# def split_tasks_by_subsection():
#   """split tasks into subsections based on attributes (i.e. tags, status, etc.)"""
#   pass 

