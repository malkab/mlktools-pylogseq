#!/bin/bash

# -----------------------------------------------------------------
#
# Executes a bash session into the Dev Container.
#
# -----------------------------------------------------------------
# The folder of the repo, as seen inside the Dev Container
# It can be checked in the console of VSC once the DC is fired
REPODIR=/workspaces/mlktools-pylogseq

if [ "$1" = "-h" ] ; then
  echo Usage: $0 [ container hash or name ] [ optional user U:G ]
  exit 0
fi

if [ -z "$1" ] ; then
  echo Specify a container hash or name and an optional user, as in 0:0 \(defaults to 1000:1000\)
  exit 2
fi

USER=1000:1000

if [ ! -z "$2" ] ; then
  USER=$2
fi

docker exec -ti \
  -u $USER \
  -w $REPODIR/src \
  $1 \
  /bin/bash
