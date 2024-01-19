#!/bin/bash


SCRIPT_PATH=$(realpath "$0")
SCRIPTS_DIR="$(dirname "$SCRIPT_PATH")"
PROJECT_DIR="$(dirname "$SCRIPTS_DIR")"
VENV_NAME="venv"
VENV_PATH="$PROJECT_DIR/$VENV_NAME"


if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_PATH
else
    echo "Virtual environment already exists at $VENV_PATH. Exiting..."
    exit 1
fi

source $VENV_PATH/bin/activate

echo "Installing dependencies..."
pip install -r "$PROJECT_DIR/requirements.txt"

read -p "Adding the executable to your path will allow you to run utilities from anywhere.  Do you want to add the executable to your path? [y/n] " response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    if [ ! $SHELL = "/bin/zsh" ]; then
        echo "This script only supports zsh."
        echo "The executable will not be added to your path. Continuing..."
    else 
        read -p "What would you like to call the executable? " executable_name


        echo "Adding executable to path..."
        ln -s $SCRIPTS_DIR/runner.sh $PROJECT_DIR/$VENV_NAME/bin/$executable_name
        chmod +x $PROJECT_DIR/$VENV_NAME/bin/$executable_name

        if [ ! -f ~/.zshenv ]; then
            touch ~/.zshenv
        fi

        echo "export PATH=$PROJECT_DIR/$VENV_NAME/bin:\$PATH" >> ~/.zshenv
    fi
fi

deactivate

# loads path to current session - this needs to be done outside the venv
source ~/.zshenv