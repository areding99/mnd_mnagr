import uuid
from mndmngr.pkm.templates.macros.Macro import Macro


class UUIDMacro(Macro):
    def resolve(self) -> str:
        return str(uuid.uuid4())

    def get_key(self) -> str:
        return "$UUID"
