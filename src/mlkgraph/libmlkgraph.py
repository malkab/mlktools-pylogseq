import glob
import os
import sys
from typing import Any, Callable

import typer
from profiles import Profiles
from pylogseq import Block, Graph, Page, PageParserError
from rich import print as pprint

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
            i, e = profiles.get_profile(p)

            for x in i:
                graphs += glob.glob(x)

            for x in e:
                graphs = list(set(graphs) - set(glob.glob(x)))

    graphs = list(set(graphs))

    # Apply glob_g in order
    for g in glob_g:
        graphs += glob.glob(g)

    graphs = list(set(graphs))

    # Apply glob_i in order
    for i in glob_i:
        graphs = list(set(graphs) - set(glob.glob(i)))

    graphs = list(set(graphs))

    return graphs
