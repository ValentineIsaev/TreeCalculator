#!/bin/bash

source .BackendVenv/bin/activate

cd backend
export PYTHONPATH=/home/inqusitor/TreeProdaction/Backend

python3 bind.py
