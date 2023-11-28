from types import ModuleType
import mndmngr.gsd.task.db_driver.read as read_driver
import mndmngr.gsd.task.db_driver.create as create_driver


def read() -> ModuleType:
    return read_driver


def create() -> ModuleType:
    return create_driver
