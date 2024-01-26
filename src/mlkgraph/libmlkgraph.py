import fnmatch
import os
import sys

# TODO
# from datetime import timedelta as td
from typing import Any, Callable

import pandas as pd
import typer
from pylogseq import Block, Graph, Page, PageParserError
from rich import print as pprint


# ----------------------
#
# Parse a group of graphs, presenting a single progress bar and
# performing operations that must be performed on all blocks.
#
# ----------------------
def parse_graph_group(
    graph_group: list[Graph], filter: Callable[[Block], bool] = lambda block: True
) -> pd.DataFrame:
    """Parses pages and blocks from a group of graphs, with error handling
    and progress indicator.

    Performs operations that must be performed on all blocks, such as searching
    for the current NOW.

    An optional lambda can be provided to filter the blocks.

    Args:
        graph_group (list[Graph]): The list of graphs to parse.
        filter (lambda, optional): A lambda filter on the block.

    Returns:
        Tuple[list[Page], list[Block]]: The lists of pages and blocks.
    """

    # Lists to store pages and blocks
    pages: list[Page] = []

    # Total pages
    for graph in graph_group:
        pages_graph: list[Page] = graph.get_pages()

        for page in pages_graph:
            pages.append(page)

    # To store final blocks
    blocks: list[dict[str, Any]] = []

    # Parse pages with progress
    with typer.progressbar(length=len(pages)) as progress:
        # Catch parsing errors
        for graph in graph_group:
            try:
                for g, p, bs in graph.parse_iter():
                    progress.update(1)

                    # Iterate blocks and check filter
                    for b in bs:
                        # Check for NOW and report
                        if b.now is True:
                            pprint(
                                f'\n[red bold]:x: NOW block "{b.title}" in page "{p.title}" in graph "{g.name}"[/]'
                            )

                        if filter(b):
                            blocks.append({"graph": g, "page": p, "block": b})

            except PageParserError as e:
                print()
                print()
                pprint("[red bold]:x: Error parsing block[/]")
                pprint("[bold]Graph:[/]")
                print(f"     {graph.name}")
                pprint("[bold]File:[/]")
                print(f"     {e.page.title}")
                pprint("[bold]Block:[/]")
                print("     " + e.block_content)
                pprint("[bold]Error:[/]")
                print("     " + str(e.original_exception))
                sys.exit(1)

    return pd.DataFrame(blocks)


# TODO: posiblemente DEPRECATED
# # ----------------------------------
# #
# # Returns the total time clocked in a period for a set of blocks.
# #
# # ----------------------------------
# def total_time_period(blocks: list[Block], period: Clock) -> td:
#     """Returns the total time clocked in a period for a set of blocks.

#     Args:
#         blocks (list[Block]): The blocks to test intersection with.
#         period (Clock): The Clock representing the period of intersection.

#     Returns:
#         td: The total time of intersection for all blocks.
#     """

#     total_time: td = td(0)

#     for block in blocks:
#         total_time += block.total_intersection_time(period)

#     return total_time


# TODO: Posibly deprecated
# # ----------------------------------
# #
# # Returns a datetime.timedelta in fraction of hours, with optional rounding.
# #
# # ----------------------------------
# def dt_to_hours(dt: td, r: int = 1) -> float:
#     """Returns a timedelta in fraction of hours, with optional rounding.

#     Args:
#         dt (td): The timedelta to convert.
#         r (int, optional): Number of decimals to round. Defaults to 1.

#     Returns:
#         float: The number of fraction of hours
#     """
#     hours = dt.total_seconds() / 3600.0

#     if r is not None:
#         return round(hours, r)
#     else:
#         return hours


# ----------------------
#
# Get graphs found in several paths and with ignore glob option.
#
# ----------------------
def get_graphs(paths: list[str], ignore_paths: list[str] | None = None) -> list[str]:
    """Get graphs found in a list of paths and filtering them with one or
    several glob patterns.

    Args:
        paths (list[str]):                  The list of paths to look for graphs
                                            in.
        ignore_paths (list[str] | None):    Optional list of globs to ignore
                                            graphs once they have been found in
                                            paths.

    Raises:
        NotImplementedError: _description_

    Returns:
        list[str]: A list of valid graph paths.
    """
    # To store found graphs in the folder
    graphs_list: list[str] = []

    # Traverse the folder tree spanning from graphs_path
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            # Check if the folder contains a "logseq" subfolder
            if "logseq" in dirnames and "journals" in dirnames and "pages" in dirnames:
                # Check last item in path is not bak
                if dirpath.split("/")[-1] != "bak":
                    graphs_list.append(dirpath)

    # No duplicates
    graphs_list = list(set(graphs_list))

    # Apply ignore globs
    if ignore_paths is not None:
        for g in ignore_paths:
            graphs_list = [path for path in graphs_list if not fnmatch.fnmatch(path, g)]

    # Final return
    return graphs_list
