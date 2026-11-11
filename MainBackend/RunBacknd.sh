#!/bin/bash

echo RUN

source treebase/.venv/bin/activate

cd treebase
export PYTHONPATH=export PYTHONPATH="$(pwd)/.."

python3 bind.py

