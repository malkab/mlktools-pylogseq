#!/bin/bash

# -----------------------------------------------------------------
#
# Install packages in pip with this script. For initializing
# VSCode Dev Containers.
#
# -----------------------------------------------------------------
# APT installs
sudo apt-get update

sudo apt-get install -y \
    git

# sudo apt-get -y upgrade

# sudo ldconfig

# sudo rm -rf /var/lib/apt/lists/*

# Update pip
/usr/local/bin/python3 -m pip install --upgrade pip

# PIP installs
/usr/local/bin/python3 -m pip install --upgrade \
    pytest \
    pytest-watch \
    build \
    marko==2.* \
    pyinstaller \
    typer[all] \
    pandas \
    jinja2 \
    arrow==1.*

# Install Wheels packages
# /usr/local/bin/python3 -m pip install \
#     whl_packages/whatever.whl \
#     whatever
