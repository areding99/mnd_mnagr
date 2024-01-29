from mndmngr.pkm.templates.macros.Macro import Macro


class HourMacro(Macro):
    def resolve(self) -> str:
        return str(self.datetime.hour)

    def get_key(self) -> str:
        return "$HOUR"
