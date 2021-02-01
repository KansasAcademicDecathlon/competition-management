#!/bin/bash
VENV_DIR="env"
if [ ! -d "$VENV_DIR" ]; then
    /c/Python27/python -m virtualenv env
fi
# shellcheck disable=SC1091
source env/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py "$@"
