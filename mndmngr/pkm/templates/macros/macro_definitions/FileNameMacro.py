from mndmngr.pkm.templates.macros.Macro import Macro


class FileNameMacro(Macro):
    def resolve(self) -> str:
        return str(self.file_name)

    def get_key(self) -> str:
        return "$F_NAME"
