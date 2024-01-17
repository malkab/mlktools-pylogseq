#!/usr/bin/env python3
# coding=UTF8

import os
from datetime import timedelta as td
from typing import Dict, List

import arrow
import typer
from libmlkgraph import parse_graph, total_time_period
from pylogseq import Block, Clock, Graph, Page
from rich import box
from rich.console import Console
from rich.table import Table

# ----------------------------------
#
# CLI application
#
# ----------------------------------

# Typer app
app = typer.Typer()


# ----------------------
#
# Command to check current week hours allocation between graphs.
#
# ----------------------
@app.command()
def projects(
    graphs_path: str = typer.Argument(".", help="The path of the graph to analyze."),
):
    # To store found graphs in the folder
    graphs_list: list[str] = []

    # Traverse the folder tree spanning from graphs_path
    for dirpath, dirnames, filenames in os.walk(graphs_path):
        # Check if the folder contains a "logseq" subfolder
        if "logseq" in dirnames and "journals" in dirnames and "pages" in dirnames:
            # Check last item in path is not bak
            if dirpath.split("/")[-1] != "bak":
                graphs_list.append(dirpath)

    # To store the total elapsed time for each graph
    times: Dict = {}

    # Iterate graphs
    for path in graphs_list:
        # Create a graph
        graph: Graph = Graph(path)

        # Get pages
        pages: list[Page] = []

        # Blocks
        blocks: list[Block] = []

        # The name of the graph
        graph_name: str = path.split("/")[-1]

        # Parse graph, with a progress bar
        print(f"\nParsing graph {graph_name}...\n")

        pages, blocks = parse_graph(graph)

        # Calculate Arrow spans for the last week
        today = arrow.now()

        span = today.span("week")
        clock = Clock(span[0].naive, span[1].naive)

        total_time: td = total_time_period(blocks, clock)

        if total_time.total_seconds() != 0:
            times[graph_name] = total_time.total_seconds() / 3600.0

    # Sum total hours
    total_hours: float = sum(times.values())

    # Data visualization
    console = Console()

    table = Table(
        title="Tiempo pasado en grafos",
        title_style="red bold",
        header_style="blue bold",
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Grafo", justify="left")
    table.add_column("Horas", justify="center")
    table.add_column("%", justify="center")

    # Ordenamos por tiempo
    sorted_times: List = sorted(times.items(), key=lambda x: x[1], reverse=True)

    for k, v in sorted_times:
        table.add_row(k, str(round(v, 1)), str(round((v / total_hours), 1)))

    table.add_row(
        "TOTAL",
        str(round(total_hours, 1)),
        str(round(total_hours / 5, 1)),
        style="red bold",
    )

    console.print(table)
    print()


# ----------------------------------
#
# Average speed in the last 4 weeks.
#
# ----------------------------------
@app.command()
def speed(
    graphs_path: str = typer.Argument(".", help="The path of the graph to analyze."),
):
    # Create a graph
    graph: Graph = Graph(graphs_path)

    # Get pages
    pages: list[Page] = []

    # Blocks
    blocks: list[Block] = []

    print("Parsing all blocks...")
    pages, blocks = parse_graph(graph)

    print()

    # To store weeks' speeds and time span
    speeds: List[float] = []
    spans: List[str] = []

    # Calculate Arrow spans for the last 4 weeks
    today = arrow.now()

    # TODO: codificado en duro para 4 semanas, posible parámetro
    for i in range(1, 5):
        # Get the clock interval spanning the week
        span = today.shift(weeks=-i).span("week")
        clock = Clock(span[0].naive, span[1].naive)

        total_time: td = total_time_period(blocks, clock)

        speeds.append(total_time.total_seconds() / 3600.0)
        spans.append(f"{span[0].format('DD-MM-YYYY')} / {span[1].format('DD-MM-YYYY')}")

    # Data visualization
    console = Console()

    table = Table(
        title="Velocidades de las últimas 4 semanas",
        title_style="red bold",
        header_style="blue bold",
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Semana", justify="left")
    table.add_column("Velocidad", justify="center")

    for i in range(len(speeds)):
        table.add_row(spans[i], str(round(speeds[i], 1)))

    table.add_row(
        "MEDIA",
        str(round(sum(speeds) / len(speeds), 1)),
        style="red bold",
    )

    console.print(table)
    print()


# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
