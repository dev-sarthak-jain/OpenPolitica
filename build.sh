#!/bin/bash

python --version
pip list

pip install -r requirements.txt
python manage.py migrate
