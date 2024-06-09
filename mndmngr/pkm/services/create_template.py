import os, sys, dotenv

dotenv.load_dotenv()
sys.path.append(os.environ["MND_MNGR_ROOT"])

from mndmngr.pkm.templates.TemplateConfigParser import TemplateConfigParser
from mndmngr.pkm.templates.parse_template import parse_template


def create_template(file_path: str, f_name: str, template_name: str) -> None:
    file_path_abs = os.path.abspath(file_path)
    user_root = os.environ["USER_ROOT"]

    if not file_path_abs.startswith(user_root):
        print("Location for file not found in project folder. Exiting...")
        sys.exit(1)

    file_path_rel = file_path_abs[len(user_root) + 1 :]

    config = TemplateConfigParser().get_config()

    if not config:
        print("No template config found. Exiting...")
        sys.exit(1)

    template = config.templates.get(template_name)

    if not template:
        print("Template not found. Exiting...")
        sys.exit(1)

    parsed_template = parse_template(
        template.body, file_path_rel, file_path_abs, f_name
    )

    with open(file_path_abs + "/" + f_name, "w") as f:
        f.write("\n".join(parsed_template))

    return None


create_template(sys.argv[1], sys.argv[2], sys.argv[3])
