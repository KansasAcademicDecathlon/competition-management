#!/bin/bash
set -e
VENV_DIR="env"

if which py; then
    python_exec="py -3"
else
    python_exec="python3"
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Virtual Environment with $python_exec"
    $python_exec -m virtualenv $VENV_DIR
fi

if [ -d $VENV_DIR/Scripts ]; then
    # shellcheck disable=SC1090
    source $VENV_DIR/Scripts/activate
else
    # shellcheck disable=SC1090
    source $VENV_DIR/bin/activate
fi

python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py "$@"
