import glob
import os
import sys
from typing import Any, Callable

import arrow
import pandas as pd
import typer
from pylogseq import Block, Clock, Graph, Page, PageParserError
from rich import print as pprint

from .profiles import Profiles

# TODO: documentar a fondo


# ----------------------
#
# Parse a group of graphs, presenting a single progress bar and
# performing operations that must be performed on all blocks.
#
# ----------------------
def parse_graph_group(
    graph_paths: list[str], filter: Callable[[Block], bool] = lambda block: True
) -> list:
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

    # To store the graphs
    graph_group: list[Graph] = [Graph(path) for path in graph_paths]

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

    return blocks


# ----------------------
#
# Get graphs found in several paths and with ignore glob option.
#
# ----------------------
def get_graphs(paths: list[str]) -> list[str]:
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

    # Final return
    return graphs_list


# ----------------------
#
# Process a list of graphs coming from a set of -p options to select the
# profiles to apply. Those can be comma-separated values.
#
# ----------------------
def process_comma_separated_options(options: list[str]) -> list[str]:
    final_options: list[str] = []

    # Untangle profiles that may be comma-separated
    for p in options:
        final_options += p.split(",")

    return final_options


# ----------------------
#
# Process final graph's paths coming from a set of -g, -p, and -i options, used
# in most of commands.
#
# ----------------------
def process_p_g_i_graph_paths(
    p_options: list[str] = [],
    g_options: list[str] = [],
    i_options: list[str] = [],
    debug: bool = False,
) -> list[str]:
    """Process inputs from the -p, -g, and -i options to return a list of
    potential paths to look for graphs in.

    Paths are processed in that order.

    Args:
        p_options (list[str], optional): List of values passed in -p options. Defaults to [].
        g_options (list[str], optional): List of values passed in -g options. Defaults to [].
        i_options (list[str], optional): List of values passed in -i options. Defaults to [].

    Returns:
        list[str]: The list of potential paths to look for graphs in.
    """
    # To store the final paths
    graphs: list[str] = []

    # Process comma-separated options
    glob_p = process_comma_separated_options(p_options)
    glob_g = process_comma_separated_options(g_options)
    glob_i = process_comma_separated_options(i_options)

    # Read profiles if any has been selected
    if len(glob_p) > 0:
        profiles: Profiles = Profiles()
        profiles.read_profiles()

        # Cycle profiles applying includes and excludes
        for p in glob_p:
            r, i, e = profiles.get_profile(p)

            for x in i:
                if debug:
                    pprint(
                        f"[green bold]Resolving include glob '{x}' for profile '{p}'[/]"
                    )
                    pprint(sorted(test_glob(r, x)))
                    print()

                graphs += test_glob(r, x)

            for x in e:
                if debug:
                    pprint(
                        f"[green bold]Resolving exclude glob '{x}' for profile '{p}'[/]"
                    )
                    pprint(sorted(test_glob(r, x)))
                    print()

                graphs = list(set(graphs) - set(test_glob(r, x)))

    graphs = list(set(graphs))

    # Apply glob_g in order
    for g in glob_g:
        if debug:
            pprint(f"[green bold]Resolving -g glob '{g}'[/]")
            pprint(sorted(glob.glob(g)))
            print()

        graphs += glob.glob(g)

    graphs = list(set(graphs))

    # Apply glob_i in order
    for i in glob_i:
        if debug:
            pprint(f"[green bold]Resolving -i glob '{i}'[/]")
            pprint(sorted(glob.glob(i)))
            print()

        graphs = list(set(graphs) - set(glob.glob(i)))

    graphs = list(set(graphs))

    return graphs


# ----------------------
#
# Tests a glob against a root path
#
# ----------------------
def test_glob(root: str, check_glob: str) -> list[str]:
    """Tests a glob against a root path.

    Args:
        root (str): The root path to test the glob against.
        glob (str): The glob to test.

    Returns:
        list[str]: glob expansion.
    """
    return glob.glob(os.path.join(root, check_glob))


# ----------------------
#
# Calculates the average speed in the last X weeks for a list of blocks.
#
# ----------------------
def calculate_speed(
    clock_blocks: list[Block], weeks: int = 4
) -> tuple[list[dict], float]:
    # Transform blocks into a DataFrame
    blocks: pd.DataFrame = pd.DataFrame(clock_blocks)

    # To store weeks' time spans
    spans: dict[str, Any] = {}

    # Calculate Arrow spans for the last 4 weeks
    today = arrow.now()

    # To store the weeks id week_x to remember how many of them are
    weeks_id: list[str] = []

    # Iterate weeks backwards
    for i in range(1, weeks + 1):
        # Get the clock interval spanning the week
        span = today.shift(weeks=-i).span("week")
        clock = Clock(span[0].naive, span[1].naive)

        # ID for the week in the spans dict and as column name
        week_id: str = f"week_{i}"
        weeks_id.append(week_id)

        # Create a column for the week
        blocks[week_id] = blocks[0].apply(
            lambda x: x.total_intersection_time(clock).total_seconds() / 3600.0
        )

        # Calculate week spans literals for presentation
        spans[
            week_id
        ] = f"{span[0].format('DD-MM-YYYY')} / {span[1].format('DD-MM-YYYY')}"

    # Calculate totals for each week
    week_speeds = blocks[weeks_id].sum()

    # Compose output
    out = []

    # Speed info for each week
    for i in range(1, weeks + 1):
        out.append({"week_id": spans[f"week_{i}"], "speed": week_speeds[f"week_{i}"]})

    # Return speed info for each week and the average of all speeds
    return (out, week_speeds.mean())
