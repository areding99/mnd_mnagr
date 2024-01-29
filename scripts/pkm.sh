#!/bin/bash

UTILITY_NAME="mnd_mngr_pkm_util"
SCRIPT_PATH=$(realpath "$0")
SCRIPTS_DIR="$(dirname "$SCRIPT_PATH")"
PROJECT_DIR="$(dirname "$SCRIPTS_DIR")"
VENV_NAME="venv"

#font
NORM=`tput sgr0`
BOLD=`tput bold`

function HELP {
    echo -e \\n"Help documentation for ${BOLD}${UTILITY_NAME}.${NORM}"\\n
    echo "The following arguments are recognized:"
    echo "-> ${BOLD}move_file${NORM}  --Accepts 1) path to the file to be moved and 2) path to the new location."
    echo "-> ${BOLD}template${NORM}  --Accepts 1) path for create location, 2) name and extension for created file, and 3) template name."
    echo -e \\n
    exit 1
}

utility=$1

source $PROJECT_DIR/$VENV_NAME/bin/activate

if [ "$utility" == "move_file" ]; then
    if [ $# -ne 3 ]; then
        HELP
    fi

    python $PROJECT_DIR/mndmngr/pkm/services/move_file.py $2 $3
elif [ "$utility" == "template" ]; then
    if [ $# -ne 4 ]; then
        HELP
    fi

    python $PROJECT_DIR/mndmngr/pkm/services/create_template.py $2 $3 $4
else
    HELP
fi
