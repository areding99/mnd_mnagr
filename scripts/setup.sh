#!/bin/bash


SCRIPT_PATH=$(realpath "$0")
SCRIPTS_DIR="$(dirname "$SCRIPT_PATH")"
UTILITY_DIR="$(dirname "$SCRIPTS_DIR")"
VENV_NAME="venv"
VENV_PATH="$UTILITY_DIR/$VENV_NAME"


if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_PATH
else
    echo "Virtual environment already exists at $VENV_PATH. Exiting..."
    exit 1
fi

source $VENV_PATH/bin/activate

echo "Installing dependencies..."
pip install -r "$UTILITY_DIR/requirements.txt"

read -p "Adding the executable to your path will allow you to run utilities from anywhere.  Do you want to add the executable to your path? [y/n] " response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    if [ ! $SHELL = "/bin/zsh" ]; then
        echo "This script only supports zsh."
        echo "The executable will not be added to your path. Continuing..."
    else 
        read -p "What would you like to call the executable? " executable_name


        echo "Adding executable to path..."
        ln -s $SCRIPTS_DIR/runner.sh $UTILITY_DIR/$VENV_NAME/bin/$executable_name
        chmod +x $UTILITY_DIR/$VENV_NAME/bin/$executable_name

        if [ ! -f ~/.zshenv ]; then
            touch ~/.zshenv
        fi

        echo "export PATH=$UTILITY_DIR/$VENV_NAME/bin:\$PATH" >> ~/.zshenv
    fi
fi

echo "Setting environment - please specify: "
read -p "- Absolute path to your project's directory: " project_dir
read -p "- Relative path (from project directory) to your tasks' folder: " tasks_rel_path
read -p "- Relative path (from project directory) to your daily logs' folder: " daily_log_rel_path


# check if the utility dir contains .env
if [ ! -f "$UTILITY_DIR/.env" ]; then
    touch "$UTILITY_DIR/.env"
fi

# write to .env
echo "PROJECT_ROOT=\"$project_dir\"" >> "$UTILITY_DIR/.env"
echo "DAILY_LOG_REL_PATH=\"$daily_log_rel_path\"" >> "$UTILITY_DIR/.env"
echo "TASKS_REL_PATH=\"$tasks_rel_path\"" >> "$UTILITY_DIR/.env"

deactivate

# loads path to current session outside the venv
source ~/.zshenv