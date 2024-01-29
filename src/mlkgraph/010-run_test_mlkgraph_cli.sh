#!/bin/bash

# # Sprint help
# ./mlkgraph.py sprint --help

# # Sprint with profiles
# ./mlkgraph.py sprint -b \
#     -i **/graph_b,**/graph_a \
#     -i "tests/**" \
#     -g "tests/**,tests/graph_b" \
#     -p profile_a_folder,c


# ./mlkgraph.py --help


# ./mlkgraph.py scrum -i **/graph_b tests/graph_a tests/graph_b tests/


# ./mlkgraph.py sprint -i **/graph_b tests/graph_a tests/graph_b tests/

# ./mlkgraph.py speed -i **/graph_b tests/graph_a tests/graph_b tests/

# profiles help
./mlkgraph.py profiles --help

# List of profiles
./mlkgraph.py profiles

# Test profiles
./mlkgraph.py profiles \
    -p profile_a_folder \
    -p profile_b \
    -g "mlkgraph_tests/**,mlkgraph_tests/graph_b" \
    -i "mlkgraph_tests/graph_b"
