import sys

import pandas as pd
import typer
from lib.constants import (
    STYLE_ROW_BACKLOG,
    STYLE_ROW_CURRENT,
    STYLE_ROW_DOING,
    STYLE_ROW_HIGHLIGHT,
    STYLE_ROW_HIGHLIGHT_SHADE,
    STYLE_ROW_NORMAL,
    STYLE_ROW_WAITING,
    STYLE_SHADE,
    STYLE_TABLE_HEADER,
    STYLE_TABLE_NAME,
    STYLE_TEXT_HIGHLIGHT,
    STYLE_TOTAL,
)
from lib.libmlkgraph import (
    calculate_speed,
    get_graphs,
    parse_graph_group,
    process_p_g_i_graph_paths,
)
from pylogseq import SCRUM_STATUS
from rich import box
from rich import print as pprint
from rich.console import Console
from rich.table import Table
from rich.text import Text


# ----------------------
#
# Command to check SCRUM marked blocks.
#
# By default it shows WAITING, DOING, and CURRENT (priority A).
# Use --backlog and --icebox to show BACKLOG and ICEBOX (priority B and C).
#
# ----------------------
def scrum(
    backlog: bool = typer.Option(False, "--backlog", "-b", help="Show backlog."),
    icebox: bool = typer.Option(False, "--icebox", "-c", help="Show icebox."),
    weeks: int = typer.Option(
        4, "--weeks", "-w", help="Number of weeks to analyze speed"
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

    # Determine target SCRUM_STATUS
    target_scrum_status: list[SCRUM_STATUS] = []

    if backlog is True:
        target_scrum_status.append(SCRUM_STATUS.BACKLOG)
    elif icebox is True:
        target_scrum_status.append(SCRUM_STATUS.ICEBOX)
    else:
        target_scrum_status = [
            SCRUM_STATUS.WAITING,
            SCRUM_STATUS.DOING,
            SCRUM_STATUS.CURRENT,
        ]

    # Get graphs in processed paths
    graphs_paths_found: list[str] = get_graphs(paths)

    # Parse blocks in graphs, getting the ones with clocks or with the target
    # SCRUM_STATUS
    blocks_parsed = parse_graph_group(
        graphs_paths_found,
        lambda x: (x.scrum_status in target_scrum_status) or (len(x.clocks) > 0),
    )

    blocks: pd.DataFrame = pd.DataFrame(blocks_parsed)

    # Calculate speed
    week_speeds, mean_speed = calculate_speed(
        [i["block"] for i in blocks_parsed if len(i["block"].clocks) > 0], weeks=weeks
    )

    # Filter blocks to get only the ones with SCRUM
    blocks = blocks[
        blocks["block"].apply(lambda x: x.scrum_status in target_scrum_status)
    ]

    print()

    # Check if there are blocks
    if blocks.empty is True:
        pprint("[red bold]No SCRUM blocks found[/]")
        sys.exit(0)

    # New column with the SCRUM status
    # Status value
    blocks["scrum_status_value"] = blocks["block"].apply(lambda x: x.scrum_status.value)

    # Status name
    blocks["scrum_status_name"] = blocks["block"].apply(lambda x: x.scrum_status.name)

    # Total time
    blocks["total_time"] = blocks["block"].apply(
        lambda x: x.total_clocked_time.total_seconds() / 3600.0
    )

    # Graph name (for sorting)
    blocks["graph_name"] = blocks["graph"].apply(lambda x: x.name)

    # Highest priority
    blocks["h_priority"] = blocks["block"].apply(lambda x: x.highest_priority)

    # Projected time
    blocks["projected_time"] = blocks["block"].apply(lambda x: x.scrum_time)

    # Remaining time
    blocks["remaining_time"] = blocks.apply(
        lambda x: max(0, (x["projected_time"] - x["total_time"])), axis=1
    )

    # Percentage of completiness
    blocks["percentage"] = blocks.apply(
        lambda row: row["total_time"] / row["block"].scrum_time
        if row["block"].scrum_time > 0
        else 0,
        axis=1,
    )

    # Sort
    blocks.sort_values(
        by=["scrum_status_value", "h_priority", "graph_name", "projected_time"],
        inplace=True,
        ascending=[False, True, True, False],
    )

    # Data visualization
    console = Console()

    table = Table(
        title="Tareas",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )
    table.add_column("Grafo", justify="left")
    table.add_column("Bloque", justify="left")
    table.add_column("Estado", justify="center")
    table.add_column("P", justify="center")
    table.add_column("TP", justify="center")
    table.add_column("TE", justify="center")
    table.add_column("TD", justify="center")
    table.add_column("%", justify="center")

    # An index to shade rows
    i: int = 0

    # Iterate rows
    for index, row in blocks.iterrows():
        if row["scrum_status_name"] == "WAITING":
            style = STYLE_ROW_WAITING
        elif row["scrum_status_name"] == "DOING":
            style = STYLE_ROW_DOING
        elif row["scrum_status_name"] == "CURRENT":
            style = STYLE_ROW_CURRENT
        elif row["scrum_status_name"] == "BACKLOG":
            style = STYLE_ROW_BACKLOG
        else:
            style = STYLE_ROW_NORMAL

        # Add shade for alternate rows
        if (i + 1) % 4 == 0:
            style += STYLE_SHADE

        # Check for priority A
        if row["block"].highest_priority == "A":
            # Shade
            if (i + 1) % 4 == 0:
                style = STYLE_ROW_HIGHLIGHT_SHADE
            else:
                style = STYLE_ROW_HIGHLIGHT

        percentage_highlighted: Text = Text(
            str(
                round(
                    row["percentage"],
                    1,
                )
            ),
            style=STYLE_TEXT_HIGHLIGHT if row["percentage"] > 1.0 else style,
        )

        table.add_row(
            row["graph"].name,
            Text(row["block"].clean_title),
            row["scrum_status_name"],
            row["block"].highest_priority,
            str(row["block"].scrum_time),
            str(round(row["total_time"], 1)),
            str(round(row["remaining_time"], 1)),
            percentage_highlighted,
            style=style,
        )

        i += 1

    # Highlight the total % if greater than 1
    total_highlighted: Text = Text(
        str(round(blocks["total_time"].sum() / blocks["projected_time"].sum(), 1)),
        style=STYLE_TEXT_HIGHLIGHT
        if round(blocks["total_time"].sum() / blocks["projected_time"].sum(), 1) > 1.0
        else STYLE_TOTAL,
    )

    table.add_row(
        "TOTAL",
        str(blocks.shape[0]),
        "-",
        "-",
        str(blocks["projected_time"].sum()),
        str(round(blocks["total_time"].sum(), 1)),
        str(round(blocks["remaining_time"].sum(), 1)),
        total_highlighted,
        style=STYLE_TOTAL,
    )

    console.print(table)

    print(
        " P: Prioridad, TP: tiempo programado, TE: tiempo empleado, TD: tiempo disponible, %: Porcentaje completado"
    )

    print()

    table = Table(show_header=False, show_lines=False, show_edge=False, pad_edge=False)

    table.add_row(
        f" Velocidad media últimas [red bold]{weeks}[/] semanas",
        f"[red bold]{round(mean_speed, 1)}[/]",
    )

    table.add_row(
        " Semanas estimadas para conclusión de tiempo restante",
        f"[red bold]{round(blocks['remaining_time'].sum() / mean_speed, 1)}[/]",
    )

    console.print(table)

    print()
