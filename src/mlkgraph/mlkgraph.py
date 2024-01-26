#!/usr/bin/env python3
# coding=UTF8

from typing import Any

import arrow
import pandas as pd
import typer
from libmlkgraph import get_graphs, parse_graph_group
from profiles import Profiles
from pylogseq import SCRUM_STATUS, Clock, Graph
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

# ----------------------
#
# Constants
#
# ----------------------
STYLE_TOTAL = "red bold on gold1"
STYLE_SHADE = " on grey82"
STYLE_TABLE_NAME = "red bold"
STYLE_TABLE_HEADER = "blue bold"
STYLE_ROW_NORMAL = "black"
STYLE_ROW_WAITING = "yellow"
STYLE_ROW_DOING = "red"
STYLE_ROW_CURRENT = "green"
STYLE_ROW_BACKLOG = "blue"
STYLE_ROW_HIGHLIGHT = "black on orange1"
STYLE_ROW_HIGHLIGHT_SHADE = "black on orange3"
STYLE_TEXT_HIGHLIGHT = "bright_white on red bold"

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
def sprint(
    graphs_paths: list[str] = typer.Argument(
        ..., help="The paths of the graph to analyze."
    ),
    ignore_paths: list[str] = typer.Option([], "--ignore", "-i", help="Ignore a path"),
    show_blocks: bool = typer.Option(
        False, "--blocks", "-b", help="Show time for blocks instead of graphs"
    ),
):
    # Get graphs in paths and ignores
    final_graphs: list[str] = get_graphs(graphs_paths, ignore_paths)

    # The list of graphs
    graphs: list[Graph] = []

    # Iterate graphs
    for path in final_graphs:
        # Create a graph
        graphs.append(Graph(path))

    # Calculate Arrow spans for the last week
    today = arrow.now()

    span = today.span("week")
    clock = Clock(span[0].naive, span[1].naive)

    # Parse blocks in graphs
    blocks: pd.DataFrame = parse_graph_group(
        graphs, lambda x: x.total_intersection_time(clock).total_seconds() > 0
    )

    # Process dataframe columns
    blocks["graph"] = blocks["graph"].apply(lambda x: x.name)
    blocks["page"] = blocks["page"].apply(lambda x: x.title)
    blocks["block_name"] = blocks["block"].apply(lambda x: x.clean_title)

    blocks["total_time"] = blocks["block"].apply(
        lambda x: x.total_intersection_time(clock).total_seconds() / 3600.0
    )

    if show_blocks is True:
        blocks = (
            blocks[["graph", "block_name", "total_time"]]
            .groupby(["graph", "block_name"])
            .sum()
        )
    else:
        blocks = blocks[["graph", "total_time"]].groupby("graph").sum()

    print()

    # Sum total hours
    total_hours: float = blocks["total_time"].sum()

    # Data visualization
    console = Console()

    # Table definition
    # Number of columns depends on block or graph view
    table = Table(
        title=f"Tiempo pasado en {'bloques' if show_blocks is True else 'grafos'} esta semana",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )

    if show_blocks is True:
        table.add_column("Grafo", justify="left")
        table.add_column("Bloque", justify="left")
        table.add_column("Horas", justify="center")
        table.add_column("%", justify="center")
    else:
        table.add_column("Grafo", justify="left")
        table.add_column("Horas", justify="center")
        table.add_column("%", justify="center")

    # Ordenamos por tiempo
    blocks.sort_values("total_time", ascending=False, inplace=True)

    # An index to shade rows
    i: int = 0

    # Iterate rows
    for index, row in blocks.iterrows():
        style = STYLE_ROW_NORMAL

        # Add shade for alternate rows
        if (i + 1) % 4 == 0:
            style += STYLE_SHADE

        if show_blocks is True:
            table.add_row(
                str(index[0]),  # type: ignore
                str(index[1]),  # type: ignore
                str(round(row["total_time"], 1)),
                str(round(row["total_time"] / total_hours, 1)),
                style=style,
            )
        else:
            table.add_row(
                index,  # type: ignore
                str(round(row["total_time"], 1)),
                str(round(row["total_time"] / total_hours, 1)),
                style=style,
            )

        i += 1

    # Total row
    if show_blocks is True:
        table.add_row(
            "TOTAL",
            "",
            str(round(total_hours, 1)),
            "-",
            style=STYLE_TOTAL,
        )
    else:
        table.add_row(
            "TOTAL",
            str(round(total_hours, 1)),
            "-",
            style=STYLE_TOTAL,
        )

    console.print(table)
    print(
        f" Horas diarias prorrateadas (5 días / semana): {round(total_hours / 5.0, 1)}"
    )
    print()


# ----------------------------------
#
# Average speed in the last 4 weeks.
#
# ----------------------------------
@app.command()
def speed(
    # graphs_path: str = typer.Argument(".", help="The path of the graph to analyze."),
    graphs_paths: list[str] = typer.Argument(
        ..., help="The paths of the graph to analyze."
    ),
    ignore_paths: list[str] = typer.Option([], "--ignore", "-i", help="Ignore a path"),
):
    # Get graphs in paths and ignores
    final_graphs: list[str] = get_graphs(graphs_paths, ignore_paths)

    # The list of graphs
    graphs: list[Graph] = []

    # Iterate graphs
    for path in final_graphs:
        # Create a graph
        graphs.append(Graph(path))

    # Parse blocks in graphs
    blocks: pd.DataFrame = parse_graph_group(graphs, lambda x: len(x.clocks) > 0)

    print()

    # To store weeks' time spans
    spans: dict[str, Any] = {}

    # Calculate Arrow spans for the last 4 weeks
    today = arrow.now()

    # TODO: codificado en duro para 4 semanas, posible parámetro
    for i in range(1, 5):
        # Get the clock interval spanning the week
        span = today.shift(weeks=-i).span("week")
        clock = Clock(span[0].naive, span[1].naive)

        # ID for the week in the spans dict and as column name
        week_id: str = f"week_{i}"

        # Create a column for the week
        blocks[week_id] = blocks["block"].apply(
            lambda x: x.total_intersection_time(clock).total_seconds() / 3600.0
        )

        spans[
            week_id
        ] = f"{span[0].format('DD-MM-YYYY')} / {span[1].format('DD-MM-YYYY')}"

    # Calculate totals for each week
    week_speeds = blocks[["week_1", "week_2", "week_3", "week_4"]].sum()

    # Data visualization
    console = Console()

    table = Table(
        title="Velocidades de las últimas 4 semanas",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Semana", justify="left")
    table.add_column("Velocidad", justify="center")

    # for i in range(len(spans)):
    #     table.add_row("JJ", "kk")

    for index, value in week_speeds.items():
        table.add_row(spans[str(index)], str(round(value, 1)))

    # Mean final row
    table.add_row(
        "MEDIA",
        str(round(week_speeds.mean(), 1)),
        style=STYLE_TOTAL,
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
    # TODO: perfil selección aquí
    p: Profiles = Profiles()

    p.read_profiles()

    # print("D: ", p.get_profile_names())

    # Get graphs in paths and ignores
    final_graphs: list[str] = get_graphs(graphs_paths, ignore_paths)

    # The list of graphs
    graphs: list[Graph] = []

    # Iterate graphs
    for path in final_graphs:
        # Create a graph
        graphs.append(Graph(path))

    # Determine target SCRUM_STATUS
    target_scrum_status: list[SCRUM_STATUS] = []

    if backlog is True:
        target_scrum_status.append(SCRUM_STATUS.BACKLOG)
    elif icebox is True:
        target_scrum_status.append(SCRUM_STATUS.ICEBOX)
    else:
        target_scrum_status = [
            SCRUM_STATUS.WAITING,
            SCRUM_STATUS.DOING,
            SCRUM_STATUS.CURRENT,
        ]

    # Parse blocks in graphs
    blocks: pd.DataFrame = parse_graph_group(
        graphs, lambda x: x.scrum_status in target_scrum_status
    )

    print()

    # New column with the SCRUM status
    if blocks.empty is False:
        # Status value
        blocks["scrum_status_value"] = blocks["block"].apply(
            lambda x: x.scrum_status.value
        )

        # Status name
        blocks["scrum_status_name"] = blocks["block"].apply(
            lambda x: x.scrum_status.name
        )

        # Total time
        blocks["total_time"] = blocks["block"].apply(
            lambda x: x.total_clocked_time.total_seconds() / 3600.0
        )

        # Graph name (for sorting)
        blocks["graph_name"] = blocks["graph"].apply(lambda x: x.name)

        # Highest priority
        blocks["h_priority"] = blocks["block"].apply(lambda x: x.highest_priority)

        # Projected time
        blocks["projected_time"] = blocks["block"].apply(lambda x: x.scrum_time)

        # Percentage of completiness
        blocks["percentage"] = blocks.apply(
            lambda row: row["total_time"] / row["block"].scrum_time
            if row["block"].scrum_time > 0
            else 0,
            axis=1,
        )

    # Sort
    blocks.sort_values(
        by=["scrum_status_value", "graph_name", "h_priority", "projected_time"],
        inplace=True,
        ascending=[False, True, True, False],
    )

    # Data visualization
    console = Console()

    table = Table(
        title="Tareas",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Grafo", justify="left")
    table.add_column("Bloque", justify="left")
    table.add_column("Estado", justify="center")
    table.add_column("P", justify="center")
    table.add_column("TP", justify="center")
    table.add_column("TE", justify="center")
    table.add_column("%", justify="center")

    # An index to shade rows
    i: int = 0

    # Iterate rows
    for index, row in blocks.iterrows():
        if row["scrum_status_name"] == "WAITING":
            style = STYLE_ROW_WAITING
        elif row["scrum_status_name"] == "DOING":
            style = STYLE_ROW_DOING
        elif row["scrum_status_name"] == "CURRENT":
            style = STYLE_ROW_CURRENT
        elif row["scrum_status_name"] == "BACKLOG":
            style = STYLE_ROW_BACKLOG
        else:
            style = STYLE_ROW_NORMAL

        # Add shade for alternate rows
        if (i + 1) % 4 == 0:
            style += STYLE_SHADE

        # Check for priority A
        if row["block"].highest_priority == "A":
            # Shade
            if (i + 1) % 4 == 0:
                style = STYLE_ROW_HIGHLIGHT_SHADE
            else:
                style = STYLE_ROW_HIGHLIGHT

        percentage_highlighted: Text = Text(
            str(
                round(
                    row["percentage"],
                    1,
                )
            ),
            style=STYLE_TEXT_HIGHLIGHT if row["percentage"] > 1.0 else style,
        )

        table.add_row(
            row["graph"].name,
            row["block"].clean_title,
            row["scrum_status_name"],
            row["block"].highest_priority,
            str(row["block"].scrum_time),
            str(round(row["total_time"], 1)),
            percentage_highlighted,
            style=style,
        )

        i += 1

    table.add_row(
        "TOTAL",
        str(blocks.shape[0]),
        "-",
        "-",
        str(blocks["projected_time"].sum()),
        str(round(blocks["total_time"].sum(), 1)),
        style=STYLE_TOTAL,
    )

    console.print(table)
    print(
        " P: Prioridad, TP: tiempo programado, TE: tiempo empleado, %: Porcentaje completado"
    )
    print()


# ----------------------
#
# Work with profiles
#
# ----------------------
@app.command()
def profiles(
    list: bool = typer.Option(False, "--list", "-l", help="List profiles"),
):
    print("D: ", list)

    p: Profiles = Profiles()

    p.read_profiles()

    df: pd.DataFrame = pd.DataFrame(p.profiles).T

    print("D: \n", df)

    # Data visualization
    console = Console()

    if list is False:
        table = Table(
            title="Profiles",
            title_style=STYLE_TABLE_NAME,
            header_style=STYLE_TABLE_HEADER,
            box=box.SIMPLE_HEAD,
        )
        table.add_column("ID", justify="left")
        table.add_column("Nombre", justify="left")
        table.add_column("Descripción", justify="left")

        # Index for shading
        for k, v in df.iterrows():
            table.add_row(str(k), v["name"], v["description"])

            print("D: ", k, v)

        SEGUIR AQUÍ

        console.print(table)


# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
