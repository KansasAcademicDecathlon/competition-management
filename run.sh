#!/bin/bash
/c/Python27/python -m virtualenv env
# shellcheck disable=SC1091
source env/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py "$@"
