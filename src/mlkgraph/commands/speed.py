import sys

import typer
from lib.constants import STYLE_TABLE_HEADER, STYLE_TABLE_NAME, STYLE_TOTAL
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
    blocks_parsed = parse_graph_group(graphs_paths_found, lambda x: len(x.clocks) > 0)

    week_speeds, mean = calculate_speed(
        [i["block"] for i in blocks_parsed], weeks=weeks
    )

    # Data visualization
    console = Console()

    table = Table(
        title=f"Velocidades de las últimas {weeks} semanas",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Semana", justify="center")
    table.add_column("Periodo", justify="left")
    table.add_column("Velocidad", justify="center")

    # An index to count weeks backwards
    week_n: int = 1

    # Add columns
    for i in week_speeds:
        table.add_row(str(-week_n), i["week_id"], str(round(i["speed"], 1)))
        week_n += 1

    # Mean final row
    table.add_row(
        "MEDIA",
        "",
        str(round(mean, 1)),
        style=STYLE_TOTAL,
    )

    console.print(table)
    print()
