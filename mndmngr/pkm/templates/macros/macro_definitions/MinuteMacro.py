from mndmngr.pkm.templates.macros.Macro import Macro


class MinuteMacro(Macro):
    def resolve(self) -> str:
        return str(self.datetime.minute)

    def get_key(self) -> str:
        return "$MINUTE"
