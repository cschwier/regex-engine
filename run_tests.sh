#!/bin/zsh
export PYTHONPATH=src/
python -m unittest discover -s ./test -p "*_test.py"
