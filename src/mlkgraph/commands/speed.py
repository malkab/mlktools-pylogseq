import sys

import typer
from lib.constants import (
    HELP_G_OPTION,
    HELP_I_OPTION,
    HELP_P_OPTION,
    STYLE_ROW_NORMAL,
    STYLE_ROW_NORMAL_SHADE,
    STYLE_TABLE_HEADER,
    STYLE_TABLE_NAME,
    STYLE_TOTAL,
)
from lib.libmlkgraph import (
    calculate_speed,
    get_graphs,
    parse_graph_group,
    process_p_g_i_graph_paths,
)
from rich import box
from rich import print as pprint
from rich.console import Console
from rich.table import Table


# ----------------------------------
#
# Average speed in the last X weeks.
#
# ----------------------------------
def speed(
    weeks: int = typer.Option(4, "--weeks", "-w", help="Number of weeks to analyze"),
    selected_profiles: list[str] = typer.Option(
        [], "--profile", "-p", help=HELP_P_OPTION
    ),
    graphs_paths: list[str] = typer.Option([], "--graph", "-g", help=HELP_G_OPTION),
    ignore_paths: list[str] = typer.Option([], "--ignore", "-i", help=HELP_I_OPTION),
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
    blocks_parsed = parse_graph_group(graphs_paths_found, lambda x: len(x.clocks) > 0)

    week_speeds, mean = calculate_speed(
        [i["block"] for i in blocks_parsed], weeks=weeks
    )

    print()

    # Data visualization
    console = Console()

    table = Table(
        title=f"Speed in the last {weeks} weeks",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Week", justify="center")
    table.add_column("Time Span", justify="left")
    table.add_column("Speed", justify="center")

    # An index to count weeks backwards
    week_n: int = 1

    # An index to shade rows
    s: int = 1

    # Add columns
    for i in week_speeds:
        # Base style
        style = STYLE_ROW_NORMAL if s % 2 != 0 else STYLE_ROW_NORMAL_SHADE

        table.add_row(
            str(-week_n), i["week_id"], str(round(i["speed"], 1)), style=style
        )
        week_n += 1
        s += 1

    # Mean final row
    table.add_row(
        "MEAN",
        "",
        str(round(mean, 1)),
        style=STYLE_TOTAL,
    )

    console.print(table)
    print()
