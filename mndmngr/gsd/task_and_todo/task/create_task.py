import os, re, datetime, uuid, dotenv, questionary
from typing import Any

if __name__ == "__main__":
  import sys
  dotenv.load_dotenv()
  sys.path.append(os.environ['PROJECT_ROOT'])

from mndmngr.gsd.task_and_todo.task.task import Task, TaskMetadata, TaskAbout
from mndmngr.config.config_parser import ConfigParser, Config

# prompt the user for a name for the task
# prompt the user for a section for the task
# prompt the user for a description for the task
# prompt the user for a priority for the task
# prompt the user for a status for the task
# prompt the user for a due date for the task
# prompt the user for a requestor for the task
# prompt the user for subscribers for the task
# prompt the user for tags for the task

def prompt_for_tag_selection() -> str:
  sections = []
  status = []
  urgency = []
  priority = []
  tags = []

  
  config: Config | None = ConfigParser().get_config()

  if (config):
    sections = config.tasks.task_subdirs_ordered
    status = config.tasks.task_config.status
    urgency = config.tasks.task_config.urgency
    priority = config.tasks.task_config.priority
    tags = config.tasks.task_config.tags


  questions: list[dict[str, Any]] = [
    {
      'type': 'text',
      'message': 'enter a title for the task',
      'name': 'title'
    },
    {
      'type': 'checkbox',
      'message': 'select a section for the task',
      'name': 'section',
      'choices': sections
    } if len(sections) > 0 else {
      'type': 'text',
      'message': 'Select a section for the task',
      'name': 'section'
    }, 
    {
      'type': 'text',
      'message': 'who requested the task?',
      'name': 'requestor'
    },
    {
      'type': 'text',
      'message': 'who is subscribed to this task?',
      'name': 'subscribers'
    },
    {
      'type': 'checkbox',
      'message': 'what is the status of this task?',
      'name': 'status',
      'choices': status
    } if len(status) > 0 else {
      'type': 'text',
      'message': 'what is the status of this task?',
      'name': 'status'
    }, 
    {
      'type': 'checkbox',
      'message': 'how urgent is this task?',
      'name': 'urgency',
      'choices': urgency
    } if len(urgency) > 0 else {
      'type': 'text',
      'message': 'how urgent is this task?',
      'name': 'urgency'
    }, 
    {
      'type': 'checkbox',
      'message': 'what is the priority of this task?',
      'name': 'priority',
      'choices': priority
    } if len(priority) > 0 else {
      'type': 'text',
      'message': 'what is the priority of this task?',
      'name': 'priority'
    }, 
    {
      'type': 'checkbox',
      'message': 'select applicable tags',
      'name': 'tags',
      'choices': tags
    } if len(sections) > 0 else {
      'type': 'text',
      'message': 'tag this task',
      'name': 'tags'
    },
    {
      'type': 'text',
      'message': 'due date?',
      'name': 'due',
      'validate': lambda val: (re.match(r"^\d{4}-\d{2}-\d{2}$", val) != None or val == "") or "date must be in the format YYYY-MM-DD"
    },
    {
      'type': 'text',
      'message': 'what\'s this task about?',
      'name': 'overview'
    }
  ]

  answers = questionary.prompt(questions)

  print(answers)

  return ""

prompt_for_tag_selection()

# don't include path to tasks folder in tasks path