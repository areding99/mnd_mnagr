from typing import TypeGuard


def is_list_of_str(obj: object) -> TypeGuard[list[str]]:
    return isinstance(obj, list) and all(isinstance(i, str) for i in obj)
