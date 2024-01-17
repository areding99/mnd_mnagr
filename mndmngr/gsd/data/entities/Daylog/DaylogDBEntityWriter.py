from mndmngr.gsd.data.entities.Daylog.DaylogDBEntity import DaylogDBEntity
from mndmngr.gsd.data.entities.Daylog.DaylogEntityData import DaylogEntityData
from mndmngr.gsd.data.entities.IDBEntity import IDBEntity
from mndmngr.gsd.data.entities.IDBEntityWriter import IDBEntityWriter
from mndmngr.gsd.data.entities.Task.TaskEntityData import TaskEntityData


class DaylogDBEntityWriter(IDBEntityWriter):
    def write(self, entity: IDBEntity) -> None:
        if not isinstance(entity, DaylogDBEntity):
            raise TypeError("entity must be of type DaylogDBEntity")

        if not entity.is_initialized():
            raise ValueError(
                "entity must be fully initialized, references are not allowed"
            )

        data = entity.get_data()

        if data is None:
            raise ValueError("data cannot be None if entity is initialized")

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
            f_io.write(f"# {data.header}")
            f_io.write("\n")
            f_io.write("\n")
            f_io.write("# tasks")
            f_io.write("\n")
            f_io.write("\n")
            for section in data.tasks:
                f_io.write(f"## {section}")
                f_io.write("\n")
                f_io.write("\n")
                for task, is_complete in data.tasks[section]:
                    if not task.is_initialized():
                        raise ValueError(
                            "task must be fully initialized, references are not allowed"
                        )

                    task_data = task.get_data()

                    if task_data is None:
                        raise TypeError("data cannot be None if task is initialized")

                    f_io.write(
                        "- ["
                        + ("x" if is_complete else " ")
                        + "] "
                        + f"[{task_data.title}]({task.get_path()})"
                    )
                    f_io.write("\n")
                f_io.write("\n")
            f_io.write("# todos")
            f_io.write("\n")
            f_io.write("\n")
            for section in data.todos:
                f_io.write(f"## {section}")
                f_io.write("\n")
                f_io.write("\n")
                for todo, is_complete in data.todos[section]:
                    f_io.write("- [" + ("x" if is_complete else " ") + "] " + todo)
                    f_io.write("\n")
                f_io.write("\n")
            f_io.write("# summary")
            f_io.write("\n")
            f_io.write("\n")
            f_io.write("## notes")
            f_io.write("\n")
            f_io.write("\n")
            f_io.write("## today's summary")
            f_io.write("\n")
            f_io.write("\n")
            f_io.write("## yesterday's summary")
            f_io.write("\n")
            f_io.write("\n")
            f_io.write(data.yesterday_summary)
