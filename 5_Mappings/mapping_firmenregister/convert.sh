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
python -m pip install git+https://github.com/anuzzolese/pyrml
python -m pip install -r ./requirements.txt
echo "✔️ installed dependencies"

# start json_to_rdf.px
echo "✔️ converted 'firmenregister.json' to 'firmenregister.n3'"
python json_to_rdf.py

# leave the virtual environment 'env'
deactivate
echo "✔️ left virtual environment 'env'"
