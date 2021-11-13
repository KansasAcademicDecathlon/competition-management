#!/bin/bash
set -e
VENV_DIR="env"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m virtualenv env
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
