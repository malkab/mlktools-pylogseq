#!/bin/bash

# -----------------------------------------------------------------
#
# Executes a bash session into the Dev Container.
#
# -----------------------------------------------------------------
# Change the ID of the DEV container here. It will change from time to
# time when it is deleted by rebuilds and such.
DEV_CONTAINER_ID=pylogseq-dev-container

# The folder of the repo, as seen inside the Dev Container
# It can be checked in the console of VSC once the DC is fired
REPODIR=/workspaces/mlktools-pylogseq

# Default user
USER=1000:1000

# Help
if [ "$1" = "-h" ] ; then
  echo As an optional parameter, an user can be provided as a parameter as U:G.
  echo Default user is 1000:1000.
  exit 0
fi

# Set user
if [ ! -z "$1" ] ; then
  USER=$1
fi

# Exec
docker exec -ti \
  -u $USER \
  -w $REPODIR/src \
  $DEV_CONTAINER_ID \
  /bin/bash
