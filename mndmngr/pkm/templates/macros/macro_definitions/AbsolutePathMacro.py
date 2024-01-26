from mndmngr.pkm.templates.macros.Macro import Macro


class AbsolutePathMacro(Macro):
    def resolve(self) -> str:
        return str(self.file_path_abs)

    def get_key(self) -> str:
        return "$ABS_PATH"
