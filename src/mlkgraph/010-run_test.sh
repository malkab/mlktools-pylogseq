#!/bin/bash

# ./mlkgraph.py sprint --help

# ./mlkgraph.py --help

# ./mlkgraph.py scrum tests/fun-fun

# ./mlkgraph.py scrum --icebox tests/fun-fun

# ./mlkgraph.py scrum -i **/graph_b tests/graph_a tests/graph_b tests/

./mlkgraph.py sprint -b -i **/graph_b tests/graph_a tests/graph_b tests/

echo

./mlkgraph.py sprint -i **/graph_b tests/graph_a tests/graph_b tests/