import sys

import pandas as pd
import typer
from lib.constants import (
    STYLE_ROW_HIGHLIGHT,
    STYLE_ROW_HIGHLIGHT_SHADE,
    STYLE_ROW_NORMAL,
    STYLE_SHADE,
    STYLE_TABLE_HEADER,
    STYLE_TABLE_NAME,
    STYLE_ROW_HIGHLIGHT_SHADE_BIS,
    STYLE_ROW_HIGHLIGHT_BIS,
    STYLE_ROW_WARNING,
    STYLE_ROW_WARNING_SHADE,
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


# ----------------------------------
#
# Average speed in the last 4 weeks.
#
# ----------------------------------
def deadline(
    selected_profiles: list[str] = typer.Option(
        [],
        "--profile",
        "-p",
        help="Profiles to apply, in order, comma-separated. Multiple -p allowed.",
    ),
    graphs_paths: list[str] = typer.Option(
        [],
        "--graph",
        "-g",
        help="Graphs to analyze, comma-separated. Multiple -g allowed. Globs can be provided.",
    ),
    ignore_paths: list[str] = typer.Option(
        [],
        "--ignore",
        "-i",
        help="Graph paths to ignore, comma-separated. Multiple -i allowed. Globs can be provided.",
    ),
):
    # Default path to local folder
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

    # Get blocks
    blocks_parsed = parse_graph_group(
        graphs_paths_found, lambda x: x.deadline is not None
    )

    # Transform blocks into a DataFrame
    blocks: pd.DataFrame = pd.DataFrame(blocks_parsed)

    print()

    # Check if there are blocks
    if blocks.empty is True:
        pprint("[red bold]No SCRUM blocks found[/]")
        sys.exit(0)

    # Graph name (for sorting)
    blocks["date"] = blocks["block"].apply(lambda x: x.deadline)

    # Days to deadline, substract deadline from today
    blocks["time_to_go"] = blocks["block"].apply(
        lambda x: (x.deadline.date() - pd.Timestamp.now().date()).days
    )

    # Sort
    blocks.sort_values(
        by=["time_to_go"],
        inplace=True,
        ascending=[True],
    )

    # Data visualization
    console = Console()

    table = Table(
        title="Deadlines",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Graph", justify="left")
    table.add_column("Page", justify="left")
    table.add_column("Block", justify="left")
    table.add_column("Deadline", justify="center")
    table.add_column("Days Left", justify="center")

    # An index to shade rows
    i: int = 0

    # Iterate rows
    for index, row in blocks.iterrows():
        style = STYLE_ROW_NORMAL

        # Add shade for alternate rows
        if (i + 1) % 4 == 0:
            style += STYLE_SHADE

        # Check times
        # By default, show time to go
        t: str = str(row["time_to_go"])

        if row["time_to_go"] < 0:
            # Shade
            if (i + 1) % 4 == 0:
                style = STYLE_ROW_WARNING_SHADE
            else:
                style = STYLE_ROW_WARNING

            # Overdue
            t = "Overdue"
        elif row["time_to_go"] < 15:
            # Shade
            if (i + 1) % 4 == 0:
                style = STYLE_ROW_HIGHLIGHT_SHADE_BIS
            else:
                style = STYLE_ROW_HIGHLIGHT_BIS
        elif row["time_to_go"] < 30:
            # Shade
            if (i + 1) % 4 == 0:
                style = STYLE_ROW_HIGHLIGHT_SHADE
            else:
                style = STYLE_ROW_HIGHLIGHT

        table.add_row(
            row["graph"].name,
            row["page"].title,
            Text(row["block"].clean_title),
            str(row["date"].strftime("%Y-%m-%d")),
            str(t),
            style=style,
        )

        i += 1

    console.print(table)
