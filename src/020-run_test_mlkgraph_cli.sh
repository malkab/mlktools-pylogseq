#!/bin/bash

export PYTHONPATH=PYTHONPATH:$(pwd)

# ---
#
# General help
#
# ---

# # mlkgraph general help
# ./mlkgraph_cli.py --help


# ---
#
# clock command
#
# ---

# # clock help
# ./mlkgraph_cli.py clock --help

# clock without options, should return results for current
# folder at graph level
./pylogseq/bin/mlkgraph_cli.py clock

# # clock with start and end dates
# ./mlkgraph_cli.py clock -s 2023-01-01 -e 2023-10-15

# # clock with start and end dates
# ./mlkgraph_cli.py clock -f "today" -b

# # clock without options, should return results for current
# # folder at block level
# ./mlkgraph_cli.py clock -b

# # clock with blocks and options
# ./mlkgraph_cli.py clock -b \
#     -i **/graph_b,**/graph_a \
#     -i "tests/**" \
#     -g "tests/**,tests/graph_b" \
#     -p profile_a_folder

# # clock without blocks and options
# ./mlkgraph_cli.py clock \
#     -p profile_b
#     # -i **/graph_b,**/graph_a \
#     # -i "tests/**" \
#     # -g "tests/**,tests/graph_b" \


# ---
#
# speed command
#
# ---

# # speed command help
# ./mlkgraph_cli.py speed --help

# # speed without options, should return results for current folder
# ./mlkgraph_cli.py speed

# # speed with week options, should return results for current folder
# ./mlkgraph_cli.py speed -w 10

# # speed with all options
# ./mlkgraph_cli.py speed -w 8 \
#     -p profile_b
#     # -i **/graph_b,**/graph_a \
#     # -i "tests/**" \
#     # -g "tests/**,tests/graph_b" \
#     # -p profile_a_folder


# ---
#
# scrum command
#
# ---

# # scrum command help
# ./mlkgraph_cli.py scrum --help

# # scrum without options, should return results for current folder
# ./mlkgraph_cli.py scrum

# # scrum with -b option, should return results for current folder
# ./mlkgraph_cli.py scrum -b

# # scrum with -c option, should return results for current folder
# ./mlkgraph_cli.py scrum -c

# # scrum with all options
# ./mlkgraph_cli.py scrum \
#     -i **/graph_b,**/graph_a \
#     -i "tests/**" \
#     -g "tests/**,tests/graph_b" \
#     -p profile_a_folder


# ---
# profiles command
# ---

# # profiles help
# ./mlkgraph_cli.py profiles --help

# # List of profiles
# ./mlkgraph_cli.py profiles

# # Test profiles
# ./mlkgraph_cli.py profiles -d \
#     -p profile_a_folder \
#     -i "./**/**b"
#     # -g mlkgraph_tests/graph_b # \
#     # -p profile_b \
#     # -i "mlkgraph_tests/graph_b"


# ---
# scheduled command
# ---

# # scheduled help
# ./mlkgraph_cli.py scheduled --help

# # No options, shows priority ones
# ./mlkgraph_cli.py scheduled

# # No options, shows non-priority ones
# ./mlkgraph_cli.py scheduled -n

# # Full options
# ./mlkgraph_cli.py scheduled -n \
#     -p profile_a_folder \
#     -i "./**/**b"


# ---
# deadline command
# ---

# # deadline help
# ./mlkgraph_cli.py deadline --help

# # No options
# ./mlkgraph_cli.py deadline

# # Full options
# ./mlkgraph_cli.py deadline \
#     -p profile_a_folder \
#     -i "./**/**b"


# ---
# grep command
# ---

# # grep help
# ./mlkgraph_cli.py grep --help

# # No options
# ./mlkgraph_cli.py grep

# # Full options
# ./mlkgraph_cli.py grep \
#     -c a
#     # -t Coursera \
#     # -p profile_a_folder \
#     # -i "./**/**b"
