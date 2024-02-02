#!/bin/bash

# -----------------------------------------------------------------
#
# Build script.
#
# -----------------------------------------------------------------
pyinstaller \
    --onefile \
    --clean \
    --collect-submodules shellingham \
    mlkgraph_cli.py
