#!/usr/bin/env python3
# coding=UTF8

import typer
import os
# from pylogseq import Graph, Page, Block, Page, PageParserError, ClockBlock
from datetime import datetime, timedelta, date
from rich.console import Console
from rich.table import Table
from enum import Enum
import pandas as pd

# For development
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pylogseq.pylogseq import Graph, Page, Block, Page, PageParserError, ClockBlock

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
    time_limit: TimeLapsesChoices = typer.Option(TimeLapsesChoices.today, "--time-limit", "-t", case_sensitive=False),
    time_aggregation: TimeAggregationChoices = typer.Option(TimeAggregationChoices.daily, "--time-aggregation", "-a", case_sensitive=False)
):
    # To store the processed graphs
    processed_graphs = []

    for graph_path in graphs:
        g = Graph(graph_path)
        g.get_pages()

        processed_graphs.append(g)

    print("D: =00", time_limit, time_aggregation)

    # Total pages
    total_pages = 0

    for g in processed_graphs:
        total_pages = total_pages + len(g.pages_file_name)

    print(f"Total number of pages to process: {total_pages}\n")

    with typer.progressbar(length=total_pages) as progress:
        for g in processed_graphs:

            # Catch parsing errors
            try:
                for p in g.parse():
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
            os.remove(page.path)

        # Warning for very small pages
        elif len(page.content) < 5:
            print(f"WARNING: page '{page.title}' in graph '{page.graph.title}' has less than 5 characters.")

    # Gather all blocks
    all_blocks: list[Block] = []

    for graph in processed_graphs:
        all_blocks.extend(graph.get_all_blocks())

    # Check for NOW blocks
    now_blocks = list(filter(lambda b: b.now, all_blocks))

    for b in now_blocks:
        print(f"WARNING: block '{b.title}' in page '{b.page.title}' of graph '{b.page.graph.title}' is in NOW state.")

    # Get time limits for today
    t = date.today()
    limitLow = datetime(t.year, t.month, t.day)
    limitHigh = datetime(t.year, t.month, t.day) + timedelta(days=1)

    # Filter all blocks with clock
    clock_blocks: list[Block] = list(filter(lambda b: len(b.logbook) > 0, all_blocks))

    # Gather all logbook entries copies of blocks
    logbook_entries: list[tuple[any, Block]] = []

    for block in clock_blocks:
        logbook_entries.extend(block.get_logbook_copies())

    # Filter blocks within the time limit
    logbook_entries_timelapse = list( \
        filter(lambda b: b.clock.start_date >= limitLow and \
               b.clock.end_date < limitHigh, logbook_entries))

    # Sort by start date
    logbook_entries_timelapse.sort(key=lambda b: b.clock.start_date)

    # Check if there is an overlapping between logbook entries
    for c in range(0, len(logbook_entries_timelapse)-1):
        if logbook_entries_timelapse[c+1].clock.start_date < logbook_entries_timelapse[c].clock.end_date:
            print(f"WARNING: block '{logbook_entries_timelapse[c+1].block.title}' in page '{logbook_entries_timelapse[c+1].block.page.title}' of graph '{logbook_entries_timelapse[c+1].block.page.graph.title}' has overlapping logbook entries with block '{logbook_entries_timelapse[c].block.title}' in page '{logbook_entries_timelapse[c].block.page.title}' of graph '{logbook_entries_timelapse[c].block.page.graph.title}': {logbook_entries_timelapse[c+1].clock.start_date} < {logbook_entries_timelapse[c].clock.end_date}")

    # Compose the Pandas dataframe data
    dataframe_data = []

    for entry in logbook_entries_timelapse:
        dataframe_data.append({
            "graph": entry.block.page.graph.title,
            "page": entry.block.page.title,
            "block": entry.block.title,
            "start_date": entry.clock.start_date,
            "end_date": entry.clock.end_date,
            "elapsed_time": entry.clock.elapsed_time,
            "allocated_time": entry.block.allocated_time,
            "time_left": entry.block.time_left,
            "tags": entry.block.tags
        })

    df = pd.DataFrame(dataframe_data)

    print("D: JUJU")
    print(df)

    print("\n\n")

    print(df.groupby("graph").agg({
        "elapsed_time": ["sum"],
        "allocated_time": ["sum"],
        "time_left": ["sum"]
    }))

    print()

    # # --------------------------------
    # # Calculate total elapsed time
    # # --------------------------------




    # # Get total time in clocks
    # total_time = {}
    # for entry in logbook_entries_timelapse_filtered:
    #     if entry.block.page.graph.title not in total_time:
    #         total_time[entry.block.page.graph.title] = entry[0].elapsed_time
    #     else:
    #         total_time[entry.block.page.graph.title] = \
    #             total_time[entry.block.page.graph.title] + \
    #             entry[0].elapsed_time

    # # --------------------------------
    # # Calculate total time allocated within the time limit
    # # --------------------------------
    # # Filter blocks with a SCHEDULED
    # scheduled_blocks: list[Block] = list(filter(lambda b: b.scheduled, all_blocks))

    # # Filter blocks within the time limit
    # scheduled_blocks_filtered = list(filter(lambda b: b.scheduled_date >= limitLow and b.scheduled_date < limitHigh, scheduled_blocks))

    # # Get total time in clocks
    # total_time_allocated = {}

    # for block in scheduled_blocks_filtered:
    #     if block.page.graph.title not in total_time_allocated:
    #         total_time_allocated[block.page.graph.title] = block.scheduled_time
    #     else:
    #         total_time_allocated[block.page.graph.title] = \
    #             total_time_allocated[block.page.graph.title] + \
    #             block.scheduled_time

    # # --------------------------------
    # # Final output
    # # --------------------------------
    # print()

    # table = Table(title="Time by graph")

    # table.add_column("Graph")
    # # table.add_colum
    # table.add_column("Elapsed time", justify="right")

    # # Sort by time
    # total_time = dict(sorted(total_time.items(), key=lambda item: item.block, reverse=True))

    # for k,v in total_time.items():
    #     table.add_row(k, str(v))

    # console = Console()
    # console.print(table)


# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
