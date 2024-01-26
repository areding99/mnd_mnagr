import os, sys, dotenv

from mndmngr.pkm.templates.macros.MacroResolver import MacroResolver

dotenv.load_dotenv()

args = sys.argv
# path to the location of the file to be created
file_path = args[1]
file_path_abs = os.path.abspath(file_path)

user_root = os.environ["USER_ROOT"]

if not file_path_abs.startswith(user_root):
    print("Location for file not found in project folder. Exiting...")
    sys.exit(1)


def create(
    file_path_rel: str, file_path_abs: str, file_name: str, template_path: str
) -> None:
    m = MacroResolver(file_path_rel, file_path_abs, file_name)
