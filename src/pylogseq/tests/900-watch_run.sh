#!/bin/bash

# -----------------------------------------------------------------
#
# Watch tests and execute them on changes.
#
# -----------------------------------------------------------------
# Tiny help
if [ "$1" = "-h" ] ; then
  echo Usage: $0 [ optional filter like \"test_a or test_b or TestClass\" ]
  exit 0
fi

# Check if there is a filter
if [ ! -z "$1" ] ; then FILTER_F="-k \"${1}\"" ; fi

# Final pytest command
COMMAND="pytest -rP -v ${FILTER_F} src"

# Run a first time
clear
eval $COMMAND

# Start watching for changes
inotifywait -r -m --exclude \.pyc -e modify src ../src | while read ; do

  eval $COMMAND

done
