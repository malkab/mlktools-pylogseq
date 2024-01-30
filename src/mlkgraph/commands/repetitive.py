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
def repetitive(
    non_priority: bool = typer.Option(
        False, "--non-priority", "-n", help="Shows non-priotity repetitives."
    ),
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
        pprint("[red bold]No SCRUM blocks found[/]")
        sys.exit(0)

    # Graph name (for sorting)
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
        title="Repetitivas prioritarias"
        if non_priority is False
        else "Repetitivas no prioritarias",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Grafo", justify="left")
    table.add_column("Bloque", justify="left")
    table.add_column("Fecha", justify="center")
    table.add_column("P", justify="center")
    table.add_column("S", justify="center")

    # An index to shade rows
    i: int = 0

    # Iterate rows
    for index, row in blocks.iterrows():
        style = STYLE_ROW_NORMAL

        # Add shade for alternate rows
        if (i + 1) % 4 == 0:
            style += STYLE_SHADE

        # Check for scores above 1
        if row["score"] >= 1.0:
            # Shade
            if (i + 1) % 4 == 0:
                style = STYLE_ROW_HIGHLIGHT_SHADE
            else:
                style = STYLE_ROW_HIGHLIGHT

        table.add_row(
            row["graph"].name,
            Text(row["block"].clean_title),
            str(row["date"].strftime("%Y-%m-%d")),
            str(row["period"]),
            str(round(row["score"], 1)),
            style=style,
        )

        i += 1

    console.print(table)

    print(" P: periodicidad en semanas, S: puntuación de retraso")

    print()
