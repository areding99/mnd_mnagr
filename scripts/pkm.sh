#!/bin/bash

UTILITY_NAME="mnd_mngr"
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
    echo "-> ${BOLD}move_file${NORM}  --Accepts a path to the file to be moved, and a path to the location to which to move the file."
    echo "-> ${BOLD}create${NORM}  --Accepts a path for location of the created note."
    echo -e \\n
    exit 1
}

if [ $# -ne 1 ]; then
    HELP
fi
