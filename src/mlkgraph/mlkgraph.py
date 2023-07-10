#!/usr/bin/env python3
# coding=UTF8

from pylogseq import Graph
import typer

# ----------------------------------
#
# CLI application
#
# ----------------------------------

# Typer app
app = typer.Typer()

# ----------------------------------
#
# Command.
#
# ----------------------------------
@app.command()
def a(
    graph_path: str = typer.Argument(..., help="The path of the graph to analyze.")
):

    print("D: graph_path: ", graph_path)















# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
