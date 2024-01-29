from mndmngr.pkm.templates.macros.Macro import Macro


class YearMacro(Macro):
    def resolve(self) -> str:
        return str(self.datetime.year)

    def get_key(self) -> str:
        return "$YEAR"
