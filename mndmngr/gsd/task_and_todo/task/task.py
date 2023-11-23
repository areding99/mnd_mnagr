from typing import NamedTuple

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
