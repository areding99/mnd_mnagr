from mndmngr.gsd.data.entities.IDBEntityData import IDBEntityData


class TaskEntityData(IDBEntityData):
    def __init__(
        self,
        title: str,
        path: str,
        created: str,
        id: str,
        requestor: str,
        subscribers: list[str],
        status: str,
        urgency: str,
        tags: list[str],
        priority: str,
        due: str,
        body: list[str],
    ):
        self.title = title
        self.path = path
        self.created = created
        self.id = id
        self.requestor = requestor
        self.subscribers = subscribers
        self.status = status
        self.urgency = urgency
        self.tags = tags
        self.priority = priority
        self.due = due
        self.body = body
