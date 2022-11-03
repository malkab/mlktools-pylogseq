#!/bin/bash

# -----------------------------------------------------------------
#
# Ejecuta una sesión bash en el Dev Container para usarla en
# terminales externos a VSCode.
#
# -----------------------------------------------------------------
docker exec -ti \
  -u 0:0 \
  -w /workspaces/mlktools-pylogseq \
  -e PYTHONPATH=$PYTHONPATH:/workspaces/mlktools-pylogseq/src \
  eloquent_agnesi \
  /bin/bash -c "./pip_install.sh"
