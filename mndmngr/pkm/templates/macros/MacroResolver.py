import os
import pkgutil
import importlib
from datetime import datetime

from mndmngr.pkm.templates.macros.Macro import Macro


class MacroResolver:
    _REL_PATH_TO_MACRO_DEFS = "/mndmngr/pkm/templates/macros/macro_defs"

    def __init__(self, file_path_rel: str, file_path_abs: str, name: str):
        self._file_path_rel = file_path_rel
        self._file_path_abs = file_path_abs
        self._date = datetime.now()
        self._name = name

        self._macro_defs_abs_path = (
            os.environ["MND_MNGR_ROOT"] + self._REL_PATH_TO_MACRO_DEFS
        )
        self._import_path = self._REL_PATH_TO_MACRO_DEFS.replace("/", ".")[1:]
        self._macros = self._get_macro_defs()

    def _get_macro_defs(self) -> dict[str, Macro]:
        macro_defs = []
        macros: dict[str, Macro] = {}

        for _, module_name, _ in pkgutil.iter_modules([self._macro_defs_abs_path]):
            module = importlib.import_module(f"{self._import_path}.{module_name}")

            class_names = [
                name
                for name, obj in vars(module).items()
                if isinstance(obj, type) and issubclass(obj, Macro) and obj is not Macro
            ]

            for class_name in class_names:
                macro_defs.append(getattr(module, class_name))

        for m_def in macro_defs:
            instance = m_def(
                self._name, self._file_path_rel, self._file_path_abs, self._date
            )
            macros[instance.get_key()] = instance

        return macros

    def get_macro_key_set(self) -> set[str]:
        return set(self._macros.keys())

    def resolve_key(self, macro: str) -> str:
        if macro not in self.get_macro_key_set():
            raise Exception(f"Macro {macro} not found")

        return self._macros[macro].resolve()
