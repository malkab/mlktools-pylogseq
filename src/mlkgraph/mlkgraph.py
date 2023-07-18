#!/usr/bin/env python3
# coding=UTF8

from pylogseq import Graph, Page, Block, Clock, PageParserError
import typer
import arrow
from datetime import timedelta as td, datetime as dt
import statistics
from rich import print as pprint
from rich.markup import escape
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich import box
import re
import pandas as pd
import sys
from libmlkgraph import *


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
def current(
    graph_path: str = typer.Argument(..., help="The path of the graph to analyze."),
    backlog: bool = typer.Option(False, "--backlog", "-b", help="Show projects with backlog."),
    # tags: list[str] = typer.Option(None, "--tag", "-t", help="A tag to filter in the tag cloud output.")
):

    # Create a graph
    graph: Graph = Graph(graph_path)

    # Get pages
    pages: list[Page] = [] #graph.get_pages()

    # Blocks
    blocks: list[Block] = []

    # Parse graph, with a progress bar
    print("\nParsing graph...\n")

    pages, blocks = parse_graph(graph)

    # Store original number of objects read from the graph
    original_number_blocks = len(blocks)
    original_number_pages = len(pages)

    print()

    # Store the blocks that has a P SCRUM project tag, since they are often
    # processed separately
    scrum_blocks: list[Block] = [ b for b in blocks if b.scrum_project is not None ]

    # Calculate the average speed of the last 4 weeks
    # TODO: hard coded 4 semanas, posible parámetro
    # Calculate Arrow spans for the last weeks
    today = arrow.now()

    # To store the total elapsed time for each of the weeks and the SCRUM
    # elapsed time
    total_elapsed_time_weeks = []
    scrum_elapsed_time_weeks = []

    # TODO: codificado en duro para 4 semanas, posible parámetro
    for i in range(1, 5):

        # Get the clock interval spanning the week
        span = today.shift(weeks=-i).span("week")
        clock = Clock(span[0].naive, span[1].naive)

        total_time: td = total_time_period(blocks, clock)
        scrum_time: td = total_time_period(scrum_blocks, clock)

        # Store
        total_elapsed_time_weeks.append(total_time.total_seconds() / 3600.0)
        scrum_elapsed_time_weeks.append(scrum_time.total_seconds() / 3600.0)

    # Filter zeros from week elapsed times
    total_elapsed_time_weeks = list(filter(lambda x: x != 0, total_elapsed_time_weeks))
    scrum_elapsed_time_weeks = list(filter(lambda x: x != 0, scrum_elapsed_time_weeks))

    # Default speeds
    # TODO: 30 horas codificado en duro, posible parámetro
    average_total_speed_last_weeks = 30
    average_scrum_speed_last_weeks = 30

    # Calculate average speed
    if total_elapsed_time_weeks != []:
        average_total_speed_last_weeks = statistics.mean(total_elapsed_time_weeks)

    if scrum_elapsed_time_weeks != []:
        average_scrum_speed_last_weeks = statistics.mean(scrum_elapsed_time_weeks)

    # Prepare the Pandas DataFrame with the following data for blocks that
    # collides with the current week and/or have P tags (Projects):
    #
    # - Block title
    # - Block tags
    # - Block SCRUM project
    # - Block SCRUM backlog time (total)
    # - Block SCRUM current time (total)
    # - Block clocked time (total)
    # - Block clocked time (this week)
    # - Block now
    # - Block done
    # - remaining_backlog_time
    # - remaining_current_time
    #
    # Therefore, the only condition to enter the data is that either the block
    # has clocked time this week or has SCRUM data.
    dataframe_data = []

    # Get current week span
    span = today.span("week")
    current_week = Clock(span[0].naive, span[1].naive)

    # Calculate total time clocked this week for all blocks and SCRUM blocks
    time_clocked_current_week: td = total_time_period(blocks, current_week)
    time_clocked_current_week_scrum: td = total_time_period(scrum_blocks, current_week)

    # Check if the backlog option is active. If not, filter out blocks
    # with no current time left
    if backlog == False:
        blocks = [ b for b in blocks if b.scrum_current_time is not None ]

    # Get block data and add to the dataframe if it qualifies
    for block in blocks:

        # Add the data if the block qualify
        # TODO: AQUÍ SE ESTÁ FILTRANDO LOS PROJECT Y NO SE ESTÁN CONTANDO LAS
        # VELOCIDADES DE TAREAS QUE NO TIENEN P EN LA SEMANA, MIRAR
        if block.scrum_project is not None:

            # Get Block data
            data = {
                    "title": block.title,
                    "tags": block.tags,
                    "scrum_project": block.scrum_project,
                    "scrum_backlog_time": block.scrum_backlog_time,
                    "scrum_current_time": block.scrum_current_time,
                    "time_clocked_total": block.total_clocked_time,
                    "time_clocked_current": block.total_intersection_time(current_week),
                    "remaining_backlog_time": block.scrum_remaining_backlog_time,
                    "remaining_current_time": block.scrum_remaining_current_time(current_week),
                    "now": block.now,
                    "done": block.done
                }

            # Check for negative remaining times
            if data["remaining_current_time"] == td(hours=0):

                pprint(f"""[bold red]:timer_clock:  WARNING![/] Block has no more available time in current
    Project:                [bright_black]{str(block.scrum_project)}[/]
    Block:                  [bright_black]{str(block.title)}[/]
    Current clocked time:   [bright_black]{dt_to_hours(data["time_clocked_current"])}[/]
    Current time:           [bright_black]{dt_to_hours(data["scrum_current_time"])}[/]
""")

            if data["remaining_backlog_time"] == td(hours=0):

                pprint(f"""[bold red]:timer_clock:  WARNING![/] Block has no more available time in backlog
    Project:                [bright_black]{str(block.scrum_project)}[/]
    Block:                  [bright_black]{str(block.title)}[/]
    Total clocked time:     [bright_black]{dt_to_hours(data["time_clocked_total"])}[/]
    Backlog time:           [bright_black]{dt_to_hours(data["scrum_backlog_time"])}[/]
""")

            # Add to the dataframe
            dataframe_data.append(data)

    # No data?
    if len(dataframe_data) == 0:
        print("No relevant blocks found.")
        sys.exit(0)

    # Create the DataFrame
    df = pd.DataFrame(dataframe_data)

    print()

    # Rich Console object
    console= Console()

    # Print general analysis
    table = Table(title="SCRUM Summary", title_style="red bold",
                  header_style="blue bold", box=box.SIMPLE_HEAD)
    table.add_column("Pages", justify="center")
    table.add_column("Blocks", justify="center")
    table.add_column("Avg Speed Total", justify="center")
    table.add_column("Avg Speed SCRUM", justify="center")
    table.add_column("Current Speed Total", justify="center")
    table.add_column("Current Speed SCRUM", justify="center")

    table.add_row(
        str(original_number_pages),
        str(original_number_blocks),
        str(round(average_total_speed_last_weeks, 1)),
        str(round(average_scrum_speed_last_weeks, 1)),
        str(dt_to_hours(time_clocked_current_week)),
        str(dt_to_hours(time_clocked_current_week_scrum)),
    )

    console.print(table)
    print()

    # Group by Project
    df_grouped = df.groupby(["scrum_project"]).sum()

    table = Table(title="SCRUM Projects", title_style="red bold",
                  header_style="blue bold", box=box.SIMPLE_HEAD,
                  footer_style="red bold", show_footer=True)
    table.add_column("Project", justify="left")
    table.add_column("Remaining Backlog", justify="center")
    table.add_column("Remaining Current", justify="center")
    table.add_column("Sprints to complete", justify="center")
    table.add_column("Sprints to complete (max)", justify="center")

    # Iterate rows
    for i, r in df_grouped.sort_index().iterrows():

        table.add_row(
                i,
                str(dt_to_hours(r["remaining_backlog_time"])),
                str(dt_to_hours(r["remaining_current_time"])),
                str(dt_to_hours(r["remaining_backlog_time"] / average_scrum_speed_last_weeks)),
                # TODO: codificado en duro para 30 horas, posible parámetro
                str(dt_to_hours(r["remaining_backlog_time"] / 30.0))
            )

    # Print table with total SCRUM times
    totals: pd.DataFrame = df.sum()

    table.add_section()

    table.add_row(
            "TOTAL",
            str(dt_to_hours(totals["remaining_backlog_time"])),
            str(dt_to_hours(totals["remaining_current_time"])),
            str(dt_to_hours(totals["remaining_backlog_time"] / average_scrum_speed_last_weeks)),
            # TODO: codificado en duro para 30 horas, posible parámetro
            str(dt_to_hours(totals["remaining_backlog_time"] / 30.0))
        , style="red bold")

    console.print(table)
    print()


# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
