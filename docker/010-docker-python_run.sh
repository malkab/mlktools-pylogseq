#/!bin/bash

# -----------------------------------------------------------------
#
# Runs an interactive Python container for development.
#
# -----------------------------------------------------------------
docker run -ti --rm \
    --name pylogseq_python_dev \
    --hostname pylogseq_python_dev \
    --user 1000:1000 \
    -v $(pwd)/../src:$(pwd)/../src \
    -v $(pwd)/../virtualenv:$(pwd)/../virtualenv \
    --workdir $(pwd)/../virtualenv \
    malkab/python:latest
