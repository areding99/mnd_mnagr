from mndmngr.pkm.templates.macros.Macro import Macro


class RelativePathMacro(Macro):
    def resolve(self) -> str:
        return str(self.file_path_rel)

    def get_key(self) -> str:
        return "$REL_PATH"
