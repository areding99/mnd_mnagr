import os, re, sys, dotenv

if __name__ == "__main__":
  sys.path.append(os.path.expanduser('~')+'/Desktop/task_management/')

from typing import NamedTuple
from mndmngr.config.config_parser import ConfigParser, Config


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



def retrieve_tasks(config: Config) -> dict[str, list[list[str]]]:
  cwd = os.getcwd()

  os.chdir(os.environ['PROJECT_ROOT']+config.tasks.file_structure.tasks_path)

  sections: list[str] = config.tasks.file_structure.ordered_subdirs
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

  os.chdir(cwd)
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

# def test(one):
#   return one



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



def get_task_infos_by_section() -> dict[str, list[TaskInfo]] | None:
  """returns a list of tasks names, organized by section & priority"""
  config: Config | None = ConfigParser().get_config()

  if (not config):
    return None

  task_mgmt_config = config.tasks
  attribute_sort_order: dict[str, list[str]] = {}

  for attr in task_mgmt_config.sort_order:
    if (hasattr(task_mgmt_config.task_config, attr)):
      attribute_sort_order[attr] = getattr(task_mgmt_config.task_config, attr) 
    else:
      attribute_sort_order[attr] = []

  raw_tasks_by_section = retrieve_tasks(config)

  parsed_tasks_by_section: dict[str, list[TaskInfo]] = {}

  for (section, raw_tasks) in raw_tasks_by_section.items():
    parsed_tasks: list[TaskInfo] = []
    for raw_task in raw_tasks:
      parsed_tasks.append(parse_task_info(raw_task))
    parsed_tasks_by_section[section] = sort_tasks(parsed_tasks, task_mgmt_config.sort_order, attribute_sort_order)

  return parsed_tasks_by_section



# TODO
# def split_tasks_by_subsection():
#   """split tasks into subsections based on attributes (i.e. tags, status, etc.)"""
#   pass 



def sort_tasks(tasks: list[TaskInfo], sort_order: list[str], intra_attr_sort_order: dict[str, list[str]]) -> list[TaskInfo]:
  return sort_tasks_impl(tasks, sort_order, intra_attr_sort_order, 0)



def sort_tasks_impl(tasks: list[TaskInfo], attrs: list[str], intra_attr_sort_order: dict[str, list[str]], attr_idx: int) -> list[TaskInfo]:
  """Recursively bucket sort tasks according sort order by attribute."""
  if (len(tasks) <= 1 or attr_idx >= len(attrs)):
    return tasks

  attr: str = attrs[attr_idx]
  attr_vals = intra_attr_sort_order[attr]
  attr_groups: dict[str, list[TaskInfo]] = {}
  attr_groups['other'] = []
  
  # bucket by attribute val
  for task in tasks:
    if hasattr(task.about_section, attr):
      attr_val = getattr(task.about_section, attr)
      if (attr_val in attr_vals):
        if (attr_val in attr_groups):
          attr_groups[attr_val].append(task)
        else:
          attr_groups[attr_val] = [task]
      else:
        attr_groups['other'].append(task)
    else: 
      # this means task doesn't have the attribute at all while the above 'other' classification just means the attribute value doesn't have a defined sort order
      raise Exception('task does not have attribute ' + attr)

  sorted_tasks: list[TaskInfo] = []

  for val in attr_vals: 
    if (val not in attr_groups):
      continue
    for task in sort_tasks_impl(attr_groups[val], attrs, intra_attr_sort_order, attr_idx+1):
      sorted_tasks.append(task)
  else:
    # these are tasks for attributes without a sort order defined on values (i.e. date due)
    # sort them in ascending order for now 
    others = attr_groups['other']
    others.sort(key=lambda t: getattr(t.about_section, attr))

    for task in others:
      sorted_tasks.append(task)

  return sorted_tasks

