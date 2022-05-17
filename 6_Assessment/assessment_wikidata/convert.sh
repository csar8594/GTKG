#!/bin/bash

# create virtual environment 'env'
python -m venv env
echo "✔️ created virtual environment 'env'"

# activate virtual environment 'env'
source env/bin/activate
echo "✔️ activated virtual environment 'env'"

# update pip
python -m pip install -U pip
echo "✔️ updated pip"

# install dependencies
python -m pip install -r ./requirements.txt
echo "✔️ installed dependencies"

# start assessing.py
echo "✔️ getting assessment results from 'firmenregister.json'"
python assessing.py

# leave the virtual environment 'env'
deactivate
echo "✔️ left virtual environment 'env'"
