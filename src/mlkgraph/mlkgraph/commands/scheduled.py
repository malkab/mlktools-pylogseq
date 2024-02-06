import sys

import pandas as pd
import typer
from mlkgraph.lib.constants import (
    COLUMN_WIDTH_GRAPH_NAME,
    HELP_G_OPTION,
    HELP_I_OPTION,
    HELP_P_OPTION,
    STYLE_ROW_NORMAL,
    STYLE_ROW_NORMAL_SHADE,
    STYLE_TABLE_HEADER,
    STYLE_TABLE_NAME,
    STYLE_TEXT_HIGHLIGHT,
)
from mlkgraph.lib.libmlkgraph import (
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
def scheduled(
    non_priority: bool = typer.Option(
        False, "--non-priority", "-n", help="Shows non-priotity repetitives."
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

    # Parse blocks in graphs
    # Check for priority or non-priority
    if non_priority is True:
        blocks_parsed = parse_graph_group(
            graphs_paths_found,
            lambda x: x.repetitive is True
            and x.repetitive_score is not None
            and x.repetitive_score >= 0,
        )
    else:
        blocks_parsed = parse_graph_group(
            graphs_paths_found,
            lambda x: x.repetitive_priority is True
            and x.repetitive_score is not None
            and x.repetitive_score >= 0,
        )

    # Transform blocks into a DataFrame
    blocks: pd.DataFrame = pd.DataFrame(blocks_parsed)

    print()

    # Check if there are blocks
    if blocks.empty is True:
        pprint("[red bold]No SCHEDULED blocks found[/]")
        sys.exit(0)

    # Date
    blocks["date"] = blocks["block"].apply(lambda x: x.scheduled)

    # Repetitive score
    blocks["score"] = blocks["block"].apply(lambda x: x.repetitive_score)

    # Repetitive period
    blocks["period"] = blocks["block"].apply(lambda x: x.repetitive_period)

    # Sort
    blocks.sort_values(
        by=["score", "period", "date"],
        inplace=True,
        ascending=[False, True, True],
    )

    # Data visualization
    console = Console()

    table = Table(
        title="Priority SCHEDULED"
        if non_priority is False
        else "Non-Priority SCHEDULED",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Graph", justify="left", max_width=COLUMN_WIDTH_GRAPH_NAME)
    table.add_column("Block", justify="left")
    table.add_column("Scheduled", justify="center")
    table.add_column("P", justify="center")
    table.add_column("S", justify="center")

    # An index to shade rows
    i: int = 1

    # Iterate rows
    for index, row in blocks.iterrows():
        # Base style
        style = STYLE_ROW_NORMAL if i % 2 != 0 else STYLE_ROW_NORMAL_SHADE

        score_hightlighted: Text = Text(
            str(
                round(
                    row["score"],
                    1,
                )
            ),
            style=STYLE_TEXT_HIGHLIGHT if row["score"] >= 1.0 else style,
        )

        table.add_row(
            row["graph"].name,
            Text(row["block"].clean_title),
            str(row["date"].strftime("%Y-%m-%d")),
            str(row["period"]),
            # str(round(row["score"], 1)),
            score_hightlighted,
            style=style,
        )

        i += 1

    console.print(table)

    print("  P: period in weeks, S: delay score")

    print()
