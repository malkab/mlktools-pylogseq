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
def sprint(
    graph_path: str = typer.Argument(..., help="The path of the graph to analyze.")
    # tags: list[str] = typer.Option(None, "--tag", "-t", help="A tag to filter in the tag cloud output.")
):

    # Create a graph
    graph: Graph = Graph(graph_path)

    # Get pages
    pages: list[Page] = graph.get_pages()

    # Blocks
    blocks: list[Block] = []

    # Parse graph, with a progress bar
    print("\nParsing graph...\n")

    with typer.progressbar(length=len(pages)) as progress:
        # Catch parsing errors
        try:
            for p, bs in graph.parse_iter():
                progress.update(1)
                blocks.extend(bs)
        except PageParserError as e:
            print()
            print()
            pprint(":WARNING: [red bold]Error parsing block[/]")
            pprint("[bold]File:[/]")
            print("     " + e.page.title)
            pprint("[bold]Error:[/]")
            print("     " + str(e.original_exception))
            pprint("[bold]Block:[/]")
            print(e.block_content)
            sys.exit(1)

    print()

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

        # To store all clocks that collides with the week span
        # Total and SCRUM clocks
        total_colliding_clocks = []
        scrum_colliding_clocks = []

        # Intersect all clocks
        for block in blocks:

            # Compute clock intersection
            inter: Clock = block.intersect_clock(clock)

            # Add to the total
            total_colliding_clocks.extend(inter)

            # Add to the SCRUM
            if block.scrum_project is not None:
                scrum_colliding_clocks.extend(inter)

        # Aggregate elapsed time
        total_time = td(0)
        scrum_time = td(0)

        for cc in total_colliding_clocks:
            total_time = total_time + cc.elapsed

        for cc in scrum_colliding_clocks:
            scrum_time = scrum_time + cc.elapsed

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

    # Get block data and add to the dataframe if it qualifies
    for block in blocks:

        # Add the data if the block qualify
        # TODO: AQUÍ SE ESTÁ FILTRANDO LOS PROJECT Y NO SE ESTÁN CONTANDO LAS
        # VELOCIDADES DE TAREAS QUE NO TIENEN P EN LA SEMANA, MIRAR
        if block.scrum_project is not None:
            # Some vars
            time_clocked_sprint = td(0)
            time_clocked_total = td(0)

            # Colliding clocks in this week
            colliding_clocks: list[Clock] = block.intersect_clock(current_week)

            # time_clocked_sprint total
            for clock in colliding_clocks:
                time_clocked_sprint += clock.elapsed

            # Calculate total clocked time
            for clock in block.clocks:
                time_clocked_total += clock.elapsed

            data = {
                    "title": block.title,
                    "tags": block.tags,
                    "scrum_project": block.scrum_project,
                    "scrum_backlog_time": block.scrum_backlog_time,
                    "scrum_current_time": block.scrum_current_time,
                    "time_clocked_total": time_clocked_total,
                    "time_clocked_sprint": time_clocked_sprint,
                    "now": block.now,
                    "done": block.done
                }

            # Calculate remaining times for backlog and current
            data["remaining_backlog_time"] = td(hours=0)
            data["remaining_current_time"] = td(hours=0)

            if block.scrum_backlog_time:
                data["remaining_backlog_time"] = block.scrum_backlog_time - \
                    time_clocked_total

            if block.scrum_current_time:
                data["remaining_current_time"] = block.scrum_current_time - \
                    time_clocked_sprint

            # Check for negative remaining times
            if data["remaining_current_time"] < td(hours=0):
                data["remaining_current_time"] = td(hours=0)

                pprint(f"""[bold red]:timer_clock:  WARNING![/] Block has no more available time in sprint
    Block:                  [bright_black]{str(block.title)}[/]
    Sprint clocked time:    [bright_black]{dt_to_hours(time_clocked_sprint)}[/]
    Current time:           [bright_black]{dt_to_hours(block.scrum_current_time)}[/]
""")

            if data["remaining_backlog_time"] < td(hours=0):
                data["remaining_backlog_time"] = td(hours=0)

                pprint(f"""[bold red]:timer_clock:  WARNING![/] Block has no more available time in backlog
    Block:                  [bright_black]{str(block.title)}[/]
    Total clocked time:     [bright_black]{dt_to_hours(time_clocked_total)}[/]
    Backlog time:           [bright_black]{dt_to_hours(block.scrum_backlog_time)}[/]
""")

            # Add to the dataframe
            dataframe_data.append(data)

    # No data?
    if len(dataframe_data) == 0:
        print("No relevant blocks found.")
        sys.exit(0)

    # Create the DataFrame
    df = pd.DataFrame(dataframe_data)

    # Print table with total SCRUM times
    totals: pd.DataFrame = df.sum()

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
    table.add_column("Current Speed", justify="center")
    table.add_column("Remaining Backlog", justify="center")
    table.add_column("Remaining Current", justify="center")
    table.add_column("Sprints to complete", justify="center")
    table.add_column("Sprints to complete (max)", justify="center")

    table.add_row(
        str(len(pages)),
        str(len(blocks)),
        str(round(average_total_speed_last_weeks, 1)),
        str(round(average_scrum_speed_last_weeks, 1)),
        str(dt_to_hours(totals["time_clocked_sprint"], 1)),
        str(dt_to_hours(totals["remaining_backlog_time"], 1)),
        str(dt_to_hours(totals["remaining_current_time"], 1)),
        str(dt_to_hours(totals["remaining_backlog_time"] / average_scrum_speed_last_weeks, 1)),
        # TODO: codificado en duro para 30 horas, posible parámetro
        str(dt_to_hours(totals["remaining_backlog_time"] / 30.0, 1))
    )

    console.print(table)
    print()

    # Group by Project
    df_grouped = df.groupby(["scrum_project"]).sum()

    table = Table(title="SCRUM Projects", title_style="red bold",
                  header_style="blue bold", box=box.SIMPLE_HEAD)
    table.add_column("Project", justify="left")
    table.add_column("Remaining Backlog", justify="center")
    table.add_column("Remaining Current", justify="center")
    table.add_column("Sprints to complete", justify="center")
    table.add_column("Sprints to complete (max)", justify="center")

    # Iterate rows
    for i, r in df_grouped.sort_index().iterrows():

        table.add_row(
            i,
            str(dt_to_hours(r["remaining_backlog_time"], 1)),
            str(dt_to_hours(r["remaining_current_time"], 1)),
            str(dt_to_hours(r["remaining_backlog_time"] / average_scrum_speed_last_weeks, 1)),
            # TODO: codificado en duro para 30 horas, posible parámetro
            str(dt_to_hours(r["remaining_backlog_time"] / 30.0, 1))
        )

    console.print(table)
    print()


# ----------------------------------
#
# Returns a datetime.timedelta in fraction of hours, with optional rounding.
#
# ----------------------------------
def dt_to_hours(dt: td, r: int=None) -> float:

    # If None, return None
    if dt is None:
        return None

    hours = dt.total_seconds() / 3600.0

    if r is not None:
        return round(hours, r)
    else:
        return hours


# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
