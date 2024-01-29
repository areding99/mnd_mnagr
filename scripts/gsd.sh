#!/bin/bash

UTILITY_NAME="mnd_mngr_gsd_util"
SCRIPT_PATH=$(realpath "$0")
SCRIPTS_DIR="$(dirname "$SCRIPT_PATH")"
PROJECT_DIR="$(dirname "$SCRIPTS_DIR")"
VENV_NAME="venv"

#font
NORM=`tput sgr0`
BOLD=`tput bold`

function HELP {
    echo -e \\n"Help documentation for ${BOLD}${UTILITY_NAME}.${NORM}"\\n
    echo "A single argument is accepted. The following arguments are recognized:"
    echo "-> ${BOLD}create_daylog${NORM}  --As named."
    echo "-> ${BOLD}create_task${NORM}  --Prompts for task details via command line to create a task file."
    echo -e \\n
    exit 1
}

if [ $# -ne 1 ]; then
    HELP
fi

utility=$1

source $PROJECT_DIR/$VENV_NAME/bin/activate

if [ "$utility" == "create_daylog" ]; then
    python $PROJECT_DIR/mndmngr/gsd/services/create_daylog.py
elif [ "$utility" == "create_task" ]; then
    python $PROJECT_DIR/mndmngr/gsd/services/create_task_cli.py
else
    HELP
fi

deactivate
