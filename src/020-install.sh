#!/bin/bash

# -----------------------------------------------------------------
#
# Installs the programs.
#
# -----------------------------------------------------------------
sudo rm /usr/local/bin/mlkgraphlog
sudo rm /usr/local/bin/mlkgraphclock
sudo cp dist/* /usr/local/bin/
