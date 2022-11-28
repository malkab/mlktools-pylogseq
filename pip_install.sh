#!/bin/bash

# -----------------------------------------------------------------
#
# Install packages in pip with this script. For initializing
# VSCode Dev Containers.
#
# -----------------------------------------------------------------
python -m pip install --upgrade pip
python -m pip install --upgrade build

pip install -U \
  marko \
  click \
  pytest \
  pyinstaller
