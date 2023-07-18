from pylogseq import Graph, Block, PageParserError, Page, Clock
import typer
from rich import print as pprint
import sys
from typing import Tuple, Callable
from datetime import timedelta as td


# ----------------------------------
#
# Parses a graph.
#
# ----------------------------------
def parse_graph(graph: Graph,
                filter: Callable[[Block], Tuple[list[Page], list[Block]]]=lambda block: True) -> \
                    Tuple[list[Page], list[Block]]:
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
            print("     " + e.page.title)
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
def dt_to_hours(dt: td, r: int=1) -> float:
    """Returns a timedelta in fraction of hours, with optional rounding.

    Args:
        dt (td): The timedelta to convert.
        r (int, optional): Number of decimals to round. Defaults to 1.

    Returns:
        float: The number of fraction of hours
    """


    # If None, return None
    if dt is None:
        return None

    hours = dt.total_seconds() / 3600.0

    if r is not None:
        return round(hours, r)
    else:
        return hours
