#!/bin/bash
set -e
VENV_DIR="env"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

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
    # shellcheck disable=SC1091
    source $VENV_DIR/Scripts/activate
else
    # shellcheck disable=SC1091
    source $VENV_DIR/bin/activate
fi

python -m pip install -q --upgrade pip
pip install -q -r "$SCRIPT_DIR"/requirements.txt
python "$SCRIPT_DIR"/main.py "$@"
