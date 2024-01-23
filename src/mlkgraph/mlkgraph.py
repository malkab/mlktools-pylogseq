#!/usr/bin/env python3
# coding=UTF8

from datetime import timedelta as td

import arrow
import typer
from libmlkgraph import parse_graph, total_time_period, get_graphs
from pylogseq import Block, Clock, Graph, Page, SCRUM_STATUS
from rich import box
from rich.text import Text
from rich.console import Console
from rich.table import Table

from typing import Any

import os

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
    graphs_paths: list[str] = typer.Argument(
        ..., help="The paths of the graph to analyze."
    ),
    ignore_paths: list[str] = typer.Option([], "--ignore", "-i", help="Ignore a path"),
):
    # Get graphs in paths and ignores
    graphs_list: list[str] = get_graphs(graphs_paths, ignore_paths)

    # To store the total elapsed time for each graph
    times: dict = {}

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
        print(f"Parsing graph {graph_name}...")

        pages, blocks = parse_graph(graph)

        # Calculate Arrow spans for the last week
        today = arrow.now()

        span = today.span("week")
        clock = Clock(span[0].naive, span[1].naive)

        total_time: td = total_time_period(blocks, clock)

        if total_time.total_seconds() != 0:
            times[graph_name] = total_time.total_seconds() / 3600.0

    print()

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
    sorted_times: list = sorted(times.items(), key=lambda x: x[1], reverse=True)

    for k, v in sorted_times:
        table.add_row(k, str(round(v, 1)), str(round((v / total_hours), 1)))

    table.add_row(
        "TOTAL",
        str(round(total_hours, 1)),
        "-",
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
    speeds: list[float] = []
    spans: list[str] = []

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


# ----------------------
#
# Command to check SCRUM marked blocks.
#
# ----------------------
@app.command()
def scrum(
    graphs_paths: list[str] = typer.Argument(
        ..., help="The paths of the graph to analyze."
    ),
    ignore_paths: list[str] = typer.Option([], "--ignore", "-i", help="Ignore a path"),
):
    # Get graphs in paths and ignores
    graphs_list: list[str] = get_graphs(graphs_paths, ignore_paths)

    # To store the total time allocated in T tags
    times: dict = {}

    # Total blocks with SCRUM with its
    scrum_blocks: dict[Graph, list[Block]] = {}

    # Iterate graphs
    for path in graphs_list:
        # Create a graph
        graph: Graph = Graph(path)

        # To store the blocks in this graph
        graph_b: list[Block] = []

        # Get pages
        pages: list[Page] = []

        # Blocks
        blocks: list[Block] = []

        # The name of the graph
        graph_name: str = path.split("/")[-1]

        # Parse graph, with a progress bar
        print(f"Parsing graph {graph_name}...")

        pages, blocks = parse_graph(graph)

        # Get blocks with SCRUM
        for b in blocks:
            if b.scrum_status not in [SCRUM_STATUS.NONE, SCRUM_STATUS.DONE]:
                graph_b.append(b)

        # Store blocks along its graph
        if len(graph_b) > 0:
            scrum_blocks[graph] = graph_b

    print()

    # Data visualization
    console = Console()

    table = Table(
        title="Tareas",
        title_style="red bold",
        header_style="blue bold",
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Grafo", justify="left")
    table.add_column("Bloque", justify="left")
    table.add_column("Estado", justify="center")
    table.add_column("Prioridad", justify="center")
    table.add_column("Tiempo programado", justify="center")
    table.add_column("Tiempo ejecutado", justify="center")

    # To store rows
    rows: list[list[Any]] = []

    # Iterate SCRUM categories
    for graph, blocks in scrum_blocks.items():
        graph_name: str = os.path.join(*graph.path.split(os.sep)[-2:])

        for b in [
            i
            for i in blocks
            if i.scrum_status is not SCRUM_STATUS.NONE and i.repetitive is False
        ]:
            rows.append(
                [
                    graph_name,
                    b.title,
                    b.scrum_status,
                    b.highest_priority,
                    b.scrum_time,
                    b.total_clocked_time,
                ]
            )

    sorted_rows: list = sorted(rows, key=lambda x: x[2].value, reverse=True)

    for r in sorted_rows:
        if r[2] == SCRUM_STATUS.WAITING:
            style = "yellow"
        elif r[2] == SCRUM_STATUS.DOING:
            style = "red"
        elif r[2] == SCRUM_STATUS.CURRENT:
            style = "green"
        elif r[2] == SCRUM_STATUS.BACKLOG:
            style = "blue"
        else:
            style = "bright_black"

        table.add_row(
            r[0],
            Text(r[1]),
            r[2].name,
            str(r[3]) if r[3] is not None else "-",
            str(r[4]),
            str(r[5]),
            style=style,
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
