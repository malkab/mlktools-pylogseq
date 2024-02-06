#!/usr/bin/env python3
# coding=UTF8

import typer
from mlkgraph.commands.clock import clock
from mlkgraph.commands.deadline import deadline
from mlkgraph.commands.grep import grep
from mlkgraph.commands.profile import profile
from mlkgraph.commands.scheduled import scheduled
from mlkgraph.commands.scrum import scrum
from mlkgraph.commands.speed import speed
from mlkgraph.lib.constants import (
    HELP_PGI_GENERAL,
)

# TODO: documentar

# Typer app
app = typer.Typer()

# ----------------------
#
# Commands
#
# ----------------------

# profiles command
app.command(
    help="""Profiles testing and listing.

    .mlkgraphprofiles are searched in the current folder and in the home folder.

    If -p, -g, and/or -i options are given, the command returns all graphs found in the resolution of given options."""
    + HELP_PGI_GENERAL
)(profile)

# scrum command
app.command(help="""SCRUM analysis.""" + HELP_PGI_GENERAL)(scrum)

# speed command
app.command(
    help="""Calculates average speed in the last N weeks (defaults to 4)."""
    + HELP_PGI_GENERAL
)(speed)

# clock command
app.command(
    help="""Check time dedication at block and graph level for a given time span (current week so far by default)."""
    + HELP_PGI_GENERAL
)(clock)

# scheduled command
app.command(
    help="""Check for SCHEDULED blocks with RA and R tags (recurring ones)."""
    + HELP_PGI_GENERAL
)(scheduled)

# deadline command
app.command(help="""Check for deadlines (DEADLINE).""" + HELP_PGI_GENERAL)(deadline)

# grep command
app.command(help="""Checks for info in blocks.""" + HELP_PGI_GENERAL)(grep)

# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
