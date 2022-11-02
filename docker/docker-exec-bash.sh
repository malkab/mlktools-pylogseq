#!/bin/bash

# -----------------------------------------------------------------
#
# Ejecuta una sesión bash en el Dev Container para usarla en
# terminales externos a VSCode.
#
# -----------------------------------------------------------------
docker exec -ti \
  -u 1000:1000 \
  -w /workspaces/mlktools-pylogseq/src \
  dazzling_galileo \
  /bin/bash
