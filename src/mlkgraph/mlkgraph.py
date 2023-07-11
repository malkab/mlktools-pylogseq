#!/usr/bin/env python3
# coding=UTF8

from pylogseq import Graph, Page
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

    # Create a graph
    graph: Graph = Graph(graph_path)

    pages: list[Page] = graph.get_pages()

    for p in pages:
        print("D: eee", p.title)
        p.read_page_file()
        p.parse()

    print("D: 3j3j", pages)











# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
