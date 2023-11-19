#!/bin/bash

python --version
pip list
poetry install
poetry run pip install -r requirements.txt
poetry run python manage.py migrate
