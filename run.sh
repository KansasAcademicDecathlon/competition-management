#!/bin/bash
VENV_DIR="env"
if [ ! -d "$VENV_DIR" ]; then
    /c/Python27/python -m virtualenv env
fi
# shellcheck disable=SC1091
source env/Scripts/activate
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt
python main.py "$@"
