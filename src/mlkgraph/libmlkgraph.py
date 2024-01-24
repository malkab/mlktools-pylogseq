import fnmatch
import os
import re
import sys
from datetime import timedelta as td
from typing import Callable

import typer
from pylogseq import Block, Clock, Graph, Page, PageParserError
from rich import print as pprint


# ----------------------------------
#
# Parses a graph.
#
# ----------------------------------
def parse_graph(
    graph: Graph,
    filter: Callable[[Block], bool] = lambda block: True,
) -> tuple[list[Page], list[Block]]:
    """Parses pages and blocks from the given graph, with error handling
    and progress indicator.

    Args:
        graph (Graph): The graph to parse.
        filter (lambda, optional): A lambda filter on the block.

    Returns:
        Tuple[list[Page], list[Block]]: The lists of pages and blocks.
    """

    # Lists to store pages and blocks
    pages: list[Page] = graph.get_pages()
    blocks: list[Block] = []

    # Progress
    with typer.progressbar(length=len(pages)) as progress:
        # Catch parsing errors
        try:
            for p, bs in graph.parse_iter():
                progress.update(1)

                # Iterate blocks and check filter
                for b in bs:
                    if filter(b):
                        blocks.append(b)

        except PageParserError as e:
            print()
            print()
            pprint("[red bold]:x: Error parsing block[/]")
            pprint("[bold]File:[/]")
            print(f"     {e.page.title}")
            pprint("[bold]Error:[/]")
            print("     " + str(e.original_exception))
            pprint("[bold]Block:[/]")
            print(e.block_content)
            sys.exit(1)

    return (pages, blocks)


# ----------------------------------
#
# Returns the total time clocked in a period for a set of blocks.
#
# ----------------------------------
def total_time_period(blocks: list[Block], period: Clock) -> td:
    """Returns the total time clocked in a period for a set of blocks.

    Args:
        blocks (list[Block]): The blocks to test intersection with.
        period (Clock): The Clock representing the period of intersection.

    Returns:
        td: The total time of intersection for all blocks.
    """

    total_time: td = td(0)

    for block in blocks:
        total_time += block.total_intersection_time(period)

    return total_time


# ----------------------------------
#
# Returns a datetime.timedelta in fraction of hours, with optional rounding.
#
# ----------------------------------
def dt_to_hours(dt: td, r: int = 1) -> float:
    """Returns a timedelta in fraction of hours, with optional rounding.

    Args:
        dt (td): The timedelta to convert.
        r (int, optional): Number of decimals to round. Defaults to 1.

    Returns:
        float: The number of fraction of hours
    """
    hours = dt.total_seconds() / 3600.0

    if r is not None:
        return round(hours, r)
    else:
        return hours


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


# ----------------------
#
# Clean the title of a block of WAITING, LATER, [#ABC] and #T tags.
#
# ----------------------
def clean_title(title: str) -> str:
    """Cleans a block title from WAITING, LATER, [#ABC] and #T tags.

    Args:
        title (str): The title to clean.

    Returns:
        str: The cleaned title.
    """

    # Drop the #T/X tags
    t = re.sub(r"#T/\d+", "", title)

    # Drop common stuff
    t: str = (
        t.replace("WAITING", "")
        .replace("LATER", "")
        .replace("NOW", "")
        .replace("**", "")
        .replace("[#A]", "")
        .replace("[#B]", "")
        .replace("[#C]", "")
        .replace("#T", "")
        .replace("#", "")
    )

    # Drop [[ and ]]
    t = t.replace("[[", "").replace("]]", "")

    return t.strip()
