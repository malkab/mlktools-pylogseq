#!/usr/bin/env python3
# coding=UTF8

import typer
from commands.profiles import profiles
from commands.scrum import scrum
from commands.speed import speed
from commands.sprint import sprint
from commands.repetitive import repetitive
from commands.deadline import deadline

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

    Globs in -pgi options must be quoted to avoid shell expansion.

    If no option -p, -g, or -i is given, the command just list
    available profiles in .mlkgraphprofiles files.

    .mlkgraphprofiles are searched in the current folder and in the home folder.

    If -p, -g, and/or -i options are given, the command returns all graphs found in the resolution
    of given options."""
)(profiles)

# scrum command
app.command(
    help="""SCRUM list.

    Globs in -pgi options must be quoted to avoid shell expansion.


    If no -pgi options are given, the command uses the current folder as the starting point to look for graphs."""
)(scrum)

# speed command
app.command(
    help="""Calculates average speed in the last N weeks (defaults to 4) for the given graphs.

    Globs in -pgi options must be quoted to avoid shell expansion.

    If no -pgi options are given, the command uses the current folder as the starting point to look for graphs."""
)(speed)

# sprint command
app.command(
    help="""Check time dedication at block and graph level for the current sprint.

            Globs in -pgi options must be quoted to avoid shell expansion.

            If no -pgi options are given, the command uses the current folder as the starting point to look for graphs."""
)(sprint)

# repetitive command
app.command(
    help="""Check for repetitive tasks.

            Globs in -pgi options must be quoted to avoid shell expansion.

            If no -pgi options are given, the command uses the current folder as the starting point to look for graphs."""
)(repetitive)

# deadline command
app.command(
    help="""Check for deadline tasks.

            Globs in -pgi options must be quoted to avoid shell expansion.

            If no -pgi options are given, the command uses the current folder as the starting point to look for graphs."""
)(deadline)

# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
