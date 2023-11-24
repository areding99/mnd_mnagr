from types import ModuleType
import mndmngr.gsd.task.db_driver.read as read_driver


def read() -> ModuleType:
    return read_driver
