from mndmngr.pkm.templates.macros.Macro import Macro


class MonthMacro(Macro):
    def resolve(self) -> str:
        return str(self.datetime.month)

    def get_key(self) -> str:
        return "$MONTH"
