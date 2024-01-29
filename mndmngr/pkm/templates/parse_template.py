from mndmngr.pkm.templates.macros.MacroResolver import MacroResolver


def parse_template(
    raw: list[str], file_path_rel: str, file_path_abs: str, file_name: str
) -> list[str]:
    """
    Parses a template by replacing macros with their respective values.
    """
    parsed: list[str] = []
    mr = MacroResolver(file_path_rel, file_path_abs, file_name)
    macro_keys = mr.get_macro_key_set()

    for i in range(len(raw)):
        line = raw[i]
        for macro_key in macro_keys:
            if macro_key in line:
                line = line.replace(macro_key, mr.resolve_key(macro_key))
        parsed.append(line)

    return parsed
