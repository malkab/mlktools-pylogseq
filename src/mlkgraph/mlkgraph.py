#!/usr/bin/env python3
# coding=UTF8

import os
from datetime import timedelta as td
from typing import Any

import arrow
import typer
from libmlkgraph import clean_title, get_graphs, parse_graph, total_time_period
from pylogseq import SCRUM_STATUS, Block, Clock, Graph, Page
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

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
# By default it shows WAITING, DOING, and CURRENT (priority A).
# Use --backlog and --icebox to show BACKLOG and ICEBOX (priority B and C).
#
# ----------------------
@app.command()
def scrum(
    graphs_paths: list[str] = typer.Argument(
        ..., help="The paths of the graph to analyze."
    ),
    ignore_paths: list[str] = typer.Option([], "--ignore", "-i", help="Ignore a path"),
    backlog: bool = typer.Option(False, "--backlog", "-b", help="Show backlog"),
    icebox: bool = typer.Option(False, "--icebox", "-c", help="Show icebox"),
):
    # Get graphs in paths and ignores
    graphs_list: list[str] = get_graphs(graphs_paths, ignore_paths)

    # Sort alphabetically
    graphs_list = sorted(graphs_list)

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
            if backlog is True:
                if b.scrum_status == SCRUM_STATUS.BACKLOG:
                    graph_b.append(b)

            elif icebox is True:
                if b.scrum_status == SCRUM_STATUS.ICEBOX:
                    graph_b.append(b)

            else:
                if b.scrum_status not in [
                    SCRUM_STATUS.NONE,
                    SCRUM_STATUS.DONE,
                    SCRUM_STATUS.BACKLOG,
                    SCRUM_STATUS.ICEBOX,
                ]:
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
    table.add_column("P", justify="center")
    table.add_column("TP", justify="center")
    table.add_column("TE", justify="center")

    # To store rows
    rows: list[list[Any]] = []

    # To store the total of clocked time, scrum time, and number of blocks
    total_scrum_time: int = 0
    total_clocked_time: td = td(0)
    total_blocks: int = 0

    # Iterate SCRUM categories
    for graph, blocks in scrum_blocks.items():
        graph_name: str = os.path.join(*graph.path.split(os.sep)[-1:])

        for b in [
            i
            for i in blocks
            if i.scrum_status is not SCRUM_STATUS.NONE and i.repetitive is False
        ]:
            rows.append(
                [
                    graph_name,
                    clean_title(b.title),
                    b.scrum_status,
                    b.highest_priority,
                    b.scrum_time,
                    b.total_clocked_time,
                ]
            )

            total_scrum_time += b.scrum_time
            total_clocked_time += b.total_clocked_time
            total_blocks += 1

    sorted_rows: list = sorted(rows, key=lambda x: x[2].value, reverse=True)

    for i, r in enumerate(sorted_rows):
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

        # Add shade for alternate rows
        if (i + 1) % 4 == 0:
            style += " on grey93"

        table.add_row(
            r[0],
            Text(r[1]),
            r[2].name,
            str(r[3]) if r[3] is not None else "-",
            str(r[4]),
            str(r[5]),
            style=style,
        )

    table.add_row(
        "TOTAL",
        str(total_blocks),
        "-",
        "-",
        str(total_scrum_time),
        str(total_clocked_time),
        style="red bold",
    )

    console.print(table)
    print("P: Prioridad, TP: tiempo programado, TE: tiempo empleado")
    print()


# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
