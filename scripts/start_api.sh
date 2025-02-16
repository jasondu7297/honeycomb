#!/bin/bash

# Identify the repo root and [cd] to the root so we are always running the script from somewhere consistent 
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export REPO_ROOT="$(cd ${SCRIPT_DIR} && git rev-parse --show-superproject-working-tree --show-toplevel | head -1)"

cd ${REPO_ROOT}

# Set the [PYTHONPATH] to the root of the [api]. Since this is our only Python project, this works nicely and solves
# our issues with module discovery.
PYTHONPATH=$(pwd)/apps/api 

# Run the [api] from the api/ directory
cd apps/api
uvicorn src.main:app --reload
