from mndmngr.gsd.data.entities.IDBEntity import IDBEntity
from mndmngr.gsd.data.entities.IDBEntityWriter import IDBEntityWriter
from mndmngr.gsd.data.entities.Task.TaskDBEntity import TaskDBEntity
from mndmngr.gsd.data.entities.Task.TaskEntityData import TaskEntityData


class TaskDBEntityWriter(IDBEntityWriter):
    _max_len_key = 11

    def write(self, entity: IDBEntity) -> None:
        if not isinstance(entity, TaskDBEntity):
            raise TypeError("entity must be of type TaskDBEntity")

        if not entity.is_initialized():
            raise ValueError(
                "entity must be fully initialized, references are not allowed"
            )

        data = entity.get_data()

        if not isinstance(data, TaskEntityData):
            raise TypeError("data must be of type TaskEntityData")

        max_len_val = self._get_max_len_val(data)

        with open(entity.get_absolute_path(), "w") as f_io:
            f_io.write("---")
            f_io.write("\n")
            f_io.write(f"title: {data.title}")
            f_io.write("\n")
            f_io.write(f"path: {data.path}")
            f_io.write("\n")
            f_io.write(f"created: {data.created}")
            f_io.write("\n")
            f_io.write(f"id: {data.id}")
            f_io.write("\n")
            f_io.write("---")
            f_io.write("\n")
            f_io.write("\n")
            f_io.write("# about")
            f_io.write("\n")
            f_io.write("\n")
            f_io.write("| " + "".ljust(self._max_len_key)+ " | " + "".ljust(max_len_val) + " |")
            f_io.write("\n")
            f_io.write("| "+ "".ljust(self._max_len_key, "-") +" | " + "".ljust(max_len_val, "-") +" |")
            f_io.write("\n")
            f_io.write(f"| {"requestor".ljust(self._max_len_key)} | {data.requestor.ljust(max_len_val)} |")
            f_io.write("\n")
            f_io.write(f"| {"subscribers".ljust(self._max_len_key)} | {", ".join(data.subscribers).ljust(max_len_val)} |")
            f_io.write("\n")
            f_io.write(f"| {"status".ljust(self._max_len_key)} | {data.status.ljust(max_len_val)} |")
            f_io.write("\n")
            f_io.write(f"| {"urgency".ljust(self._max_len_key)} | {data.urgency.ljust(max_len_val)} |")
            f_io.write("\n")
            f_io.write(f"| {"tags".ljust(self._max_len_key)} | {", ".join(data.tags).ljust(max_len_val)} |")
            f_io.write("\n")
            f_io.write(f"| {"priority".ljust(self._max_len_key)} | {data.priority.ljust(max_len_val)} |")
            f_io.write("\n")
            f_io.write(f"| {"due".ljust(self._max_len_key)} | {data.due.ljust(max_len_val)} |")
            f_io.write("\n")
            f_io.write("\n")
            f_io.write("".join(data.body))

    def _get_max_len_val(self, data: TaskEntityData) -> int:
        max_leng_val = 0

        if len(data.requestor) > max_leng_val:
            max_leng_val = len(data.requestor)

        if len(", ".join(data.subscribers)) > max_leng_val:
            max_leng_val = len(", ".join(data.subscribers))

        if len(data.status) > max_leng_val:
            max_leng_val = len(data.status)

        if len(data.urgency) > max_leng_val:
            max_leng_val = len(data.urgency)

        if len(", ".join(data.tags)) > max_leng_val:
            max_leng_val = len(", ".join(data.tags))

        if len(data.priority) > max_leng_val:
            max_leng_val = len(data.priority)

        if len(data.due) > max_leng_val:
            max_leng_val = len(data.due)

        return max_leng_val
