#!/bin/bash

# -----------------------------------------------------------------
#
# Builds the package.
#
# -----------------------------------------------------------------
python -m build

pip install --force-reinstall dist/pylogseq-0.0.1-py3-none-any.whl
