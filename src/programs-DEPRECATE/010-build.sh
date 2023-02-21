#!/bin/bash

# -----------------------------------------------------------------
#
# Build script.
#
# -----------------------------------------------------------------
pyinstaller --onefile --clean mlkgraphlog/mlkgraphlog.py

pyinstaller --onefile --clean mlkgraphclock/mlkgraphclock.py
