import os, re
from typing import NamedTuple, Any
from library.config_parser import ConfigParser, Config

# types
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

class TaskInfo(NamedTuple):
  metadata: TaskMetadata
  about_section: TaskAbout



def retrieve_tasks(parent_dir: str, task_path: str, ordered_subdirs: list[str]) -> dict[str, list[list[str]]]:
  os.chdir(os.path.expanduser('~')+parent_dir+task_path)

  sections: list[str] = ordered_subdirs

  sections_with_tasks: dict[str, list[list[str]]] = {}
  
  for section in sections:
      os.chdir(section)
      task_files = os.listdir()

      tasks: list[list[str]] = []
      for t_file in task_files:
        with open (t_file, 'r') as f_io:
          tasks.append(f_io.readlines())
      sections_with_tasks[section] = tasks
      os.chdir("..")

  return sections_with_tasks 



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



def parse_task_info(raw_task: list[str]) -> TaskInfo:
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

  return TaskInfo(parse_metadata_section(metadata_section), parse_about_section(about_section))



def get_tasks_and_info() -> None:
  """returns a list of tasks names, organized by section & priority"""
  config: Config | None = ConfigParser().get_config()

  if (not config):
    return None

  lib_config = config.lib
  task_mgmt_config = config.tasks

  raw_tasks_by_section = retrieve_tasks(lib_config.parent_dir, task_mgmt_config.file_structure.tasks_path, task_mgmt_config.file_structure.ordered_subdirs)

  parsed_tasks_by_section: dict[str, list[TaskInfo]] = {}

  for (section, raw_tasks) in raw_tasks_by_section.items():
    parsed_tasks: list[TaskInfo] = []
    for raw_task in raw_tasks:
      parsed_tasks.append(parse_task_info(raw_task))
    parsed_tasks_by_section[section] = parsed_tasks




get_tasks_and_info()


