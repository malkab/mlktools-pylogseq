#!/usr/bin/env python3
# coding=UTF8

import typer
import os
from pylogseq import Clock, Graph, Page, Block, Page, PageParserError, ArrayBlock
from datetime import datetime, timedelta, date
from rich.console import Console
from rich.text import Text
from rich.table import Table
from enum import Enum
import pandas as pd

# Typer app
app = typer.Typer()

# Time lapses option choices
class TimeLapsesChoices(str, Enum):
    today = "today"
    week = "week"
    month = "month"
    year = "year"

# Time aggregation option choices
class TimeAggregationChoices(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"

# ----------------------------------
#
# Command to check time spent in each graph.
#
# ----------------------------------
@app.command()
def clock(
    graphs: list[str] = typer.Argument(..., help="List of graphs to parse."),
    time_limit: TimeLapsesChoices = typer.Option(TimeLapsesChoices.week, "--time-limit", "-t", case_sensitive=False),
    time_aggregation: TimeAggregationChoices = typer.Option(TimeAggregationChoices.daily, "--time-aggregation", "-a", case_sensitive=False),
    verbose: bool = typer.Option(False, "--verbose", "-v", case_sensitive=False)
):

    # To store the processed graphs
    processed_graphs = []

    # Get graphs
    for graph_path in graphs:
        g = Graph(graph_path)
        processed_graphs.append(g)

    # Total pages, getting them
    total_pages = 0

    for g in processed_graphs:
        total_pages = total_pages + len(g.get_pages())

    print(f"Total number of pages to process: {total_pages}\n")

    with typer.progressbar(length=total_pages) as progress:
        for g in processed_graphs:

            # Catch parsing errors
            try:
                for p in g.parse_iter():
                    progress.update(1)
            except PageParserError as e:
                print()
                print("Error parsing block")
                print("File: ", e.page.title)
                print("Error: ", e.original_exception)
                print("Block:\n", e.block_content)

    print()

    # Gather all pages in graphs to check for small content
    all_pages: list[Page] = []

    for graph in processed_graphs:
        all_pages.extend(graph.pages)

    # Delete pages with content = 0
    for page in all_pages:
        if len(page.content) == 0 or page.content == "-\n" or page.content == "-":
            print(f"WARNING: page '{page.title}' in graph '{page.graph.title}' has no content, deleting it.")
            os.remove(page.abs_path)

        # Warning for very small pages
        elif len(page.content) < 5:
            print(f"WARNING: page '{page.title}' in graph '{page.graph.title}' has less than 5 characters.")

    # Gather all blocks and create an ArrayBlock
    all_blocks: list[Block] = []

    for graph in processed_graphs:
        all_blocks.extend(graph.get_all_blocks())

    ab = ArrayBlock(all_blocks)

    # Check for NOW blocks
    now_blocks = list(filter(lambda b: b.now, ab))

    for b in now_blocks:
        print(f"WARNING: block '{b.title}' in page '{b.page.title}' of graph '{b.page.graph.title}' is in NOW state.")

    # Process the time lapse interval: today, week, month, year
    # Today
    if time_limit == TimeLapsesChoices.today:
        start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

    # Week
    if time_limit == TimeLapsesChoices.week:
        now = datetime.now()
        days_since_monday = (now.weekday() - 0) % 7
        last_monday = now - timedelta(days=days_since_monday)
        start = datetime(last_monday.year, last_monday.month, last_monday.day)
        end = start + timedelta(days=7)

    # Month
    if time_limit == TimeLapsesChoices.month:
        now = datetime.now()
        start = datetime(now.year, now.month, 1)
        end = start + timedelta(days=31)

    # Get all ClockBlocks hitting the interval
    clock_blocks = ab.get_clock_blocks(filter_interval=Clock(start, end))

    # Sort by start date
    clock_blocks.sort(key=lambda b: b.clock.start)

    # Check if there is an overlapping between logbook entries
    for c in range(0, len(clock_blocks)-1):
        if clock_blocks[c+1].clock.start < clock_blocks[c].clock.end:
            print(f"WARNING: block '{clock_blocks[c+1].block.title}' in page '{clock_blocks[c+1].block.page.title}' of graph '{clock_blocks[c+1].block.page.graph.title}' has overlapping logbook entries with block '{clock_blocks[c].block.title}' in page '{clock_blocks[c].block.page.title}' of graph '{clock_blocks[c].block.page.graph.title}': {clock_blocks[c+1].clock.start} < {clock_blocks[c].clock.end}")

    # Compose the Pandas dataframe data
    dataframe_data = []

    for entry in clock_blocks:
        dataframe_data.append({
            "id": entry.block.id,
            "elapsed_time": entry.clock.elapsed
        })

    # Check if the DF is empty: no colliding time intervals
    if len(dataframe_data) == 0:
        print("No colliding time intervals found.")
        sys.exit(0)

    df = pd.DataFrame(dataframe_data)

    # Filter the ID in the all_blocks
    all_blocks_filtered = list(filter(lambda b: b.id in df["id"].values, all_blocks))

    # Create another DF with the filtered blocks
    df_all_blocks_filtered_data = []

    for entry in all_blocks_filtered:
        df_all_blocks_filtered_data.append({
            "id": entry.id,
            "graph": entry.page.graph.title,
            "block": entry.title,
            "highest_priority": entry.highest_priority,
            "allocated_time": entry.allocated_time,
            "time_left": entry.time_left_hours,
            "tags": entry.tags
        })

    df_all_blocks_filtered = pd.DataFrame(df_all_blocks_filtered_data)

    # Group by ID and sum the elapsed time
    df = df.groupby("id").agg(elapsed_time=("elapsed_time", "sum"))

    # Merge the DF with the elapsed_time sum with the DF with the filtered blocks
    df_merge = df_all_blocks_filtered.join(df, on="id")

    if verbose:
        table = Table(title="Blocks")

        table.add_column("Graph")
        table.add_column("Block")
        table.add_column("P", justify="center")
        table.add_column("Allocated time", justify="center")
        table.add_column("Time left", justify="center")
        table.add_column("Elapsed time", justify="center")

        # Reset the index and sort by ellapsed time
        verbose=df_merge.reset_index().sort_values(by="elapsed_time", ascending=False)

        # Add rows
        for k,v in verbose.iterrows():
            table.add_row(v["graph"], Text(v["block"]), v['highest_priority'],
                          str(v["allocated_time"]),
                          f"{str(round(v['time_left'], 1))} hours",
                          str(v["elapsed_time"]))

        # Print
        console = Console()
        console.print(table)

    # Do the final aggregation of allocated_time, time_left, and elapsed_time
    # by id
    final = df_merge[[ "graph", "allocated_time", "time_left", "elapsed_time" ]] \
        .groupby("graph").agg(
            allocated_time=("allocated_time", "sum"),
            time_left=("time_left", "sum"),
            elapsed_time=("elapsed_time", "sum")
        )

    # --------------------------------
    # Final output in a table
    # --------------------------------
    print()

    table = Table(title="Time by graph")

    table.add_column("Graph")
    table.add_column("Allocated time", justify="right")
    table.add_column("Time left", justify="right")
    table.add_column("Elapsed time", justify="right")

    # Reset the index and sort by ellapsed time
    final = final.reset_index().sort_values(by="elapsed_time", ascending=False)

    # Add rows
    for k,v in final.iterrows():
        table.add_row(v["graph"], str(v["allocated_time"]),
                      str(round(v["time_left"], 1)),
                      str(v["elapsed_time"]))

    # Print
    console = Console()
    console.print(table)

    # --------------------------------
    # Final
    # --------------------------------
    print()

    # Sum all columns
    final = final[[ "allocated_time", "time_left", "elapsed_time" ]].sum()

    # Calculate days since last monday, max 5 days per week
    if time_limit == TimeLapsesChoices.today:
        days = 1

    if time_limit == TimeLapsesChoices.week:
        now = datetime.now()
        days_since_monday = (now.weekday() - 0) % 7
        days = min(5, days_since_monday + 1)

    if time_limit == TimeLapsesChoices.month:
        weeks = datetime.now().day / 7.0
        days = 5 * weeks

    final["per_day"] = round(((final["elapsed_time"] / days).total_seconds() / 3600.0), 1)

    table = Table(title="Totals and daily average")

    table.add_column("Allocated time", justify="center")
    table.add_column("Time left", justify="center")
    table.add_column("Elapsed time", justify="center")
    table.add_column("Elapsed time per day", justify="center")

    # Add row
    table.add_row(str(final["allocated_time"]),
                    str(round(final["time_left"], 1)),
                    str(final["elapsed_time"]),
                    str(f'{final["per_day"]} hours'))

    # Print
    console = Console()
    console.print(table)

# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
