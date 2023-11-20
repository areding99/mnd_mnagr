import os, re, sys, dotenv

if __name__ == "__main__":
  dotenv.load_dotenv()
  sys.path.append(os.environ['PROJECT_ROOT'])

from typing import NamedTuple
from mndmngr.config.config_parser import ConfigParser, Config


########################
# RETRIEVAL
########################


def retrieve_tasks_section(section: str) -> list[list[str]]:
  cwd = os.getcwd()

  os.chdir(os.environ['TASKS_PATH'])
  os.chdir(section)

  task_files = os.listdir()

  tasks: list[list[str]] = []

  for t_file in task_files:
    with open (t_file, 'r') as f_io:
      tasks.append(f_io.readlines())

  os.chdir(cwd)

  return tasks

########################
# PARSING
########################

class TaskMetadata(NamedTuple):
  title: str
  path: str
  created: str
  id: str

class TaskAbout(NamedTuple):
  requestor: str
  subscribers: list[str]
  status: str
  urgency: str
  priority: str
  tags: list[str]
  due: str

class Task(NamedTuple):
  metadata: TaskMetadata
  about_section: TaskAbout
  raw_task: list[str]


def parse_metadata_section(section: list[str]) -> TaskMetadata:
  title: str = ""
  path: str = ""
  created: str = ""
  id: str = ""

  for line in section:
    l = re.split(r":", line, 1)
    key = l[0].strip()
    val = l[1].strip()
  
    match key:
      case "title":
        title = val
      case "path":
        path = val
      case "created":
        created = val
      case "id":
        id = val

  return TaskMetadata(title, path, created, id)


def parse_about_section(section: list[str]) -> TaskAbout:
  requestor: str = ""
  subscribers: list[str] = []
  status: str = ""
  urgency: str = ""
  priority: str = ""
  tags: list[str] = []
  due: str = ""

  for line in section:
    l = re.split(r"\|", line)
    key = l[1].strip()
    val = l[2].strip()

    match key:
      case "requestor":
        requestor = val
      case "subscribers":
        for v in val.split(","):
          subscribers.append(v.strip())
      case "status":
        status = val
      case "urgency":
        urgency = val
      case "priority":
        priority = val
      case "tags":
        for v in val.split(","):
          tags.append(v.strip())
      case "due":
        due = val

  return TaskAbout(requestor, subscribers, status, urgency, priority, tags, due)



def parse_task(raw_task: list[str]) -> Task:
  metadata_section: list[str] = []
  in_metadata: bool = False
  about_section: list[str] = []
  in_about: bool = False

  for line in raw_task:
    if (line.startswith('---')):
      in_metadata = False

    if (in_metadata):
      metadata_section.append(line)

    if (line.startswith('---') and len(metadata_section) == 0):
      in_metadata = True

    if (line == '\n' and in_about):
        break

    if (in_about):
      about_section.append(line)

    if (re.match(r"(\|\s*-+\s*){2}\|", line) and len(about_section) == 0):
      in_about = True

  return Task(parse_metadata_section(metadata_section), parse_about_section(about_section), raw_task=raw_task)

########################
# RETRIVAL AND PARSING
########################

def retrieve_parse_all_tasks() -> dict[str, list[Task]]:
  config: Config | None = ConfigParser().get_config()

  if (not config):
    return {}

  sections: list[str] = config.tasks.task_subdirs_ordered
  sections_with_tasks: dict[str, list[Task]] = {}
  
  for section in sections:
      for task in retrieve_tasks_section(section):
        if section not in sections_with_tasks:
          sections_with_tasks[section] = []
        sections_with_tasks[section].append(parse_task(task))


  return sections_with_tasks 