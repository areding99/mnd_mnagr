import json

from typing import NamedTuple, Any, TypeGuard

class LibSection(NamedTuple):
  parent_dir: str

class DailyLogFS(NamedTuple):
  daily_log_path: str

class DailyLogSection(NamedTuple):
  file_structure: DailyLogFS

class TasksFS(NamedTuple):
  tasks_path: str
  ordered_subdirs: list[str]

class TaskConfig(NamedTuple):
  status_enum: list[str]
  urgency_enum: list[str]
  priority_enum: list[str]
  tags_enum: list[str]

class TasksSection(NamedTuple):
  file_structure: TasksFS
  task_config: TaskConfig

class Config(NamedTuple):
  lib: LibSection
  daily_log: DailyLogSection
  tasks: TasksSection

class ConfigParser(object):
  _instance = None
  config: Config | None = None
  def __new__(cls):
    if not isinstance(cls._instance, cls):
      cls._instance = object.__new__(cls)
    return cls._instance

  def get_config(self) -> Config | None: 
    if (self.config is not None):
      return self.config

    with open("./config.json") as f_io:
      self.config = ConfigParser.parse_config(json.load(f_io))

    return self.config

  @staticmethod
  def parse_config(config_json: Any) -> Config:
    if (not config_json):
      raise Exception('config is empty')
    
    lib_section_parent_dir = config_json['lib']['parent_dir']

    if not isinstance(lib_section_parent_dir, str):
      raise Exception('config does not match expected format')


    daily_log_fs_path = config_json['daily_log']['file_structure']['daily_log_path']

    if not isinstance(daily_log_fs_path, str):
      raise Exception('config does not match expected format')

    tasks_fs_path = config_json['tasks']['file_structure']['tasks_path']

    if not isinstance(tasks_fs_path, str):
      raise Exception('config does not match expected format')

    tasks_fs_ordered_subdirs = config_json['tasks']['file_structure']['ordered_subdirs']

    if not is_list_of_str(tasks_fs_ordered_subdirs):
      raise Exception('config does not match expected format')

    tasks_config_status_enum = config_json['tasks']['task_config']['status_enum']

    if not is_list_of_str(tasks_config_status_enum):
      raise Exception('config does not match expected format') 

    tasks_config_urgency_enum = config_json['tasks']['task_config']['urgency_enum']

    if not is_list_of_str(tasks_config_urgency_enum):
      raise Exception('config does not match expected format')

    tasks_config_priority_enum = config_json['tasks']['task_config']['priority_enum']

    if not is_list_of_str(tasks_config_priority_enum):
      raise Exception('config does not match expected format')

    tasks_config_tags_enum = config_json['tasks']['task_config']['tags_enum']

    if not is_list_of_str(tasks_config_tags_enum):
      raise Exception('config does not match expected format')  

    return Config(
      lib=LibSection(
        parent_dir=lib_section_parent_dir
      ),
      daily_log=DailyLogSection(
        file_structure=DailyLogFS(
          daily_log_path=daily_log_fs_path
        )
      ),
      tasks=TasksSection(
        file_structure=TasksFS(
          tasks_path=tasks_fs_path,
          ordered_subdirs=tasks_fs_ordered_subdirs
        ),
        task_config=TaskConfig(
          status_enum=tasks_config_status_enum,
          urgency_enum=tasks_config_urgency_enum,
          priority_enum=tasks_config_priority_enum,
          tags_enum=tasks_config_tags_enum
        )
      )
    )

# TODO move this into its own module -
def is_list_of_str(obj: object) -> TypeGuard[list[str]]:
  return isinstance(obj, list) and all(isinstance(i, str) for i in obj)






     
   






