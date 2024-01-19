# takes args & runs a given script based on the passed args


SCRIPT_PATH=$(realpath "$0")
SCRIPTS_DIR="$(dirname "$SCRIPT_PATH")"
PROJECT_DIR="$(dirname "$SCRIPTS_DIR")"
VENV_NAME="venv_mnd_mngr"

# activate
# source $PROJECT_DIR/$VENV_NAME/bin/activate

echo "running"



