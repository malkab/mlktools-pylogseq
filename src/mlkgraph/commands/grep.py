import sys

import pandas as pd
import typer
from lib.constants import (
    HELP_G_OPTION,
    HELP_I_OPTION,
    HELP_P_OPTION,
    STYLE_ROW_NORMAL,
    STYLE_ROW_NORMAL_SHADE,
    STYLE_TABLE_HEADER,
    STYLE_TABLE_NAME,
    COLUMN_WIDTH_GRAPH_NAME,
    COLUMN_WIDTH_PAGE_NAME,
)
from lib.libmlkgraph import (
    get_graphs,
    parse_graph_group,
    process_p_g_i_graph_paths,
)
from rich import box
from rich import print as pprint
from rich.console import Console
from rich.table import Table
from rich.text import Text


# ----------------------
#
# Command to check info, for example, words in a block title or content.
#
# ----------------------
def grep(
    title: list[str] = typer.Option(
        None,
        "--title",
        "-t",
        help="Word to search in the title. Can be given multiple times.",
    ),
    content: list[str] = typer.Option(
        None,
        "--content",
        "-c",
        help="Word to search in the content. Can be given multiple times.",
    ),
    selected_profiles: list[str] = typer.Option(
        [],
        "--profile",
        "-p",
        help=HELP_P_OPTION,
    ),
    graphs_paths: list[str] = typer.Option(
        [],
        "--graph",
        "-g",
        help=HELP_G_OPTION,
    ),
    ignore_paths: list[str] = typer.Option(
        [],
        "--ignore",
        "-i",
        help=HELP_I_OPTION,
    ),
):
    # Default path to local
    paths = ["."]

    if not (
        len(selected_profiles) == 0
        and len(graphs_paths) == 0
        and len(ignore_paths) == 0
    ):
        # Process pgi options
        try:
            paths: list[str] = process_p_g_i_graph_paths(
                selected_profiles, graphs_paths, ignore_paths
            )
        except Exception as e:
            pprint(f"[red bold]{e}[/]")
            sys.exit(1)

    # Get graphs in processed paths
    graphs_paths_found: list[str] = get_graphs(paths)

    # Define filtering lambda
    lam: list = []  # noqa: E731
    table_title: list[str] = []

    # Check for title search
    if len(title) > 0:
        for t in title:
            lam.append(lambda x: t in x.title)
            table_title.append(f"[green bold]'{t}'[/] in the title")

    if len(content) > 0:
        for c in content:
            lam.append(lambda x: c in x.content)
            table_title.append(f"[green bold]'{c}'[/] in the content")

    if len(title) == 0 and len(content) == 0:
        pprint("[red bold]Error:[/] no search term provided")
        sys.exit(0)

    # Final blocks
    blocks_parsed = []

    for la in lam:
        blocks_parsed = blocks_parsed + parse_graph_group(graphs_paths_found, la)

    # Transform blocks into a DataFrame
    blocks: pd.DataFrame = pd.DataFrame(blocks_parsed)

    # No blocks
    if len(blocks) == 0:
        pprint("[red bold]No blocks found.[/]")
        sys.exit(0)

    # Add new columns
    # For sorting
    blocks["graph_name"] = blocks["graph"].apply(lambda x: x.name)

    blocks["page_title"] = blocks["page"].apply(lambda x: x.title)

    blocks["block_clean_title"] = blocks["block"].apply(lambda x: x.clean_title)

    blocks["repetitive"] = blocks["block"].apply(lambda x: "x" if x.repetitive else "")

    blocks["priority"] = blocks["block"].apply(
        lambda x: x.highest_priority if x.highest_priority is not None else ""
    )

    # Sort
    blocks.sort_values(
        by=["graph_name", "page_title", "block_clean_title"],
        inplace=True,
        ascending=[True, True, True],
    )

    print()

    # Data visualization
    console = Console()

    table = Table(
        title=f"Blocks with {' + '.join(table_title)}",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Graph", justify="left", max_width=COLUMN_WIDTH_GRAPH_NAME)
    table.add_column("Page", justify="left", max_width=COLUMN_WIDTH_PAGE_NAME)
    table.add_column("Block", justify="left")
    table.add_column("S", justify="center")
    table.add_column("P", justify="center")

    # An index to shade rows
    i: int = 1

    for index, row in blocks.iterrows():
        # Base style
        style = STYLE_ROW_NORMAL if i % 2 != 0 else STYLE_ROW_NORMAL_SHADE

        table.add_row(
            row["graph_name"],
            row["page_title"],
            Text(row["block_clean_title"]),
            row["repetitive"],
            row["priority"],
            style=style,
        )

        i += 1

    console.print(table)

    print("  S: SCHEDULED, P: highest priority")

    print()
