#!/bin/bash


SCRIPT_PATH=$(realpath "$0")
SCRIPTS_DIR="$(dirname "$SCRIPT_PATH")"
ROOT="$(dirname "$SCRIPTS_DIR")"
VENV_NAME="venv"
VENV_PATH="$ROOT/$VENV_NAME"


if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_PATH
else
    echo "Virtual environment already exists at $VENV_PATH. Exiting..."
    exit 1
fi

source $VENV_PATH/bin/activate

read -p "Starting the project in 'dev' mode will install dependecies used in development only.  Do you want to start the project in 'dev' mode? [y/n] " dev_mode_response

echo "Installing dependencies..."
pip install -r "$ROOT/requirements/common.txt"

if [[ "$dev_mode_response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    echo "Installing dev dependencies..."
    pip install -r "$ROOT/requirements/dev.txt"
else 
    echo "Installing prod dependencies..."
    pip install -r "$ROOT/requirements/prod.txt"
fi


read -p "Adding the executable to your path will allow you to run utilities from anywhere.  Do you want to add the executable to your path? [y/n] " update_path_response

if [[ "$update_path_response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    if [ ! $SHELL = "/bin/zsh" ]; then
        echo "This script only supports zsh."
        echo "The executable will not be added to your path. Continuing..."
    else 
        read -p "What would you like to call the gsd executable? " gsd_executable_name

        echo "Adding gsd executable to path..."
        ln -s $SCRIPTS_DIR/gsd.sh $ROOT/$VENV_NAME/bin/$gsd_executable_name
        chmod +x $ROOT/$VENV_NAME/bin/$gsd_executable_name


        read -p "What would you like to call the pkm executable? " pkm_executable_name

        echo "Adding pkm executable to path..."
        ln -s $SCRIPTS_DIR/pkm.sh $ROOT/$VENV_NAME/bin/$pkm_executable_name
        chmod +x $ROOT/$VENV_NAME/bin/$pkm_executable_name


        if [ ! -f ~/.zshenv ]; then
            touch ~/.zshenv
        fi

        echo "export PATH=$ROOT/$VENV_NAME/bin:\$PATH" >> ~/.zshenv
    fi
fi

echo "Setting environment - please specify: "
read -p "- Absolute path to your project's directory: " user_root
read -p "- Relative path (from project directory) to your tasks' folder: " tasks_rel_path
read -p "- Relative path (from project directory) to your daily logs' folder: " daily_log_rel_path
read -p "- Relative path (from project directory) to your notes' folder: " notes_rel_path


# check if the utility dir contains .env
if [ ! -f "$ROOT/.env" ]; then
    touch "$ROOT/.env"
fi

# write to .env
echo "MND_MNGR_ROOT=\"$ROOT\"" >> "$ROOT/.env"
echo "USER_ROOT=\"$user_root\"" >> "$ROOT/.env"
echo "TASKS_REL_PATH=\"$tasks_rel_path\"" >> "$ROOT/.env"
echo "DAILY_LOG_REL_PATH=\"$daily_log_rel_path\"" >> "$ROOT/.env"
echo "NOTES_REL_PATH=\"$notes_rel_path\"" >> "$ROOT/.env"

deactivate

# loads path to current session outside the venv
source ~/.zshenv