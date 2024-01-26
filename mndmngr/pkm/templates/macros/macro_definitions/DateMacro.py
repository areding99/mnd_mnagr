from mndmngr.pkm.templates.macros.Macro import Macro


class DateMacro(Macro):
    def resolve(self) -> str:
        return str(self.datetime.day)

    def get_key(self) -> str:
        return "$DATE"
