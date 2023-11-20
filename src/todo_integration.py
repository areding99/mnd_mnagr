import os, uuid
from src.library.config_parser import ConfigParser, Config


def get_todos_by_section() -> dict[str, list[str]] | None:
  config: Config | None = ConfigParser().get_config()

  if (not config):
    return None

  cwd = os.getcwd()
  parent_dir = config.lib.parent_dir
  todo_path = config.todos.file_structure.todos_path
  os.chdir(os.path.expanduser('~')+parent_dir+todo_path)

  todos_by_section: dict[str, list[str]] = {}

  for file in os.listdir():
    todos: list[str] = []

    with open (file, 'r') as f_io:
      todos.append(f_io.readlines())
    
    



  os.chdir(cwd) 
  pass

# def retrieve_tasks(parent_dir: str, task_path: str, ordered_subdirs: list[str]) -> dict[str, list[list[str]]]:
#   cwd = os.getcwd()
#   os.chdir(os.path.expanduser('~')+parent_dir+task_path)

#   sections: list[str] = ordered_subdirs
#   sections_with_tasks: dict[str, list[list[str]]] = {}
  
#   for section in sections:
#       os.chdir(section)
#       task_files = os.listdir()

#       tasks: list[list[str]] = []
#       for t_file in task_files:
#         with open (t_file, 'r') as f_io:
#           tasks.append(f_io.readlines())
#       sections_with_tasks[section] = tasks
#       os.chdir("..")

#   os.chdir(cwd)
#   return sections_with_tasks 


def remove_finished_todos() -> None:
  pass



# each todo has a unique id so that changes to the todo doesn't disrupt the integration with the daily log
# probably between 4-8 characters so not distracting
def get_id() -> str:
  return str(uuid.uuid4())