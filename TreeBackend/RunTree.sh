#!/bin/bash

echo RUN

source .TreeVenv/bin/activate

cd treebase
export PYTHONPATH=/home/inqusitor/TreeProdaction/TreeBase

python3 bind.py
