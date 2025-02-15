#!/bin/bash

# create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install project dependencies
source install_python_deps.sh
