#!/bin/bash

# -----------------------------------------------------------------
#
# Install packages in pip with this script. For initializing
# VSCode Dev Containers.
#
# -----------------------------------------------------------------
# APT installs
# sudo apt-get update

# sudo apt-get install -y \
#   something

# sudo apt-get -y upgrade

# sudo ldconfig

# sudo rm -rf /var/lib/apt/lists/*

# PIP installs
python -m pip install --upgrade pip
python -m pip install --upgrade build

pip install -U \
  marko \
  pytest \
  pytest-watch \
  pyinstaller \
  typer[all]
