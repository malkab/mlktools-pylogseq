import sys

import pandas as pd
import typer
from pylogseq.mlkgraph.lib.constants import (
    COLUMN_WIDTH_GRAPH_NAME,
    COLUMN_WIDTH_PAGE_NAME,
    HELP_B_OPTION,
    HELP_G_OPTION,
    HELP_I_OPTION,
    HELP_P_OPTION,
    STYLE_ROW_NORMAL,
    STYLE_ROW_NORMAL_SHADE_MODIFIER,
    STYLE_ROW_SCRUM_BACKLOG,
    STYLE_ROW_SCRUM_CURRENT,
    STYLE_ROW_SCRUM_DOING,
    STYLE_ROW_SCRUM_WAITING,
    STYLE_TABLE_HEADER,
    STYLE_TABLE_NAME,
    STYLE_TEXT_HIGHLIGHT,
    STYLE_TOTAL,
)
from pylogseq.mlkgraph.lib.libmlkgraph import (
    calculate_speed,
    get_graphs,
    parse_graph_group,
    process_p_g_i_graph_paths,
)
from pylogseq.pylogseq import SCRUM_STATUS
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
    current: bool = typer.Option(
        False,
        "--current",
        "-u",
        help="Show only current status and up, ignoring Backlog.",
    ),
    icebox: bool = typer.Option(False, "--icebox", "-c", help="Show icebox."),
    show_blocks: bool = typer.Option(False, "--blocks", "-b", help=HELP_B_OPTION),
    weeks: int = typer.Option(
        4, "--weeks", "-w", help="Number of weeks to analyze speed"
    ),
    selected_profiles: list[str] = typer.Option(
        [], "--profile", "-p", help=HELP_P_OPTION
    ),
    graphs_paths: list[str] = typer.Option([], "--graph", "-g", help=HELP_G_OPTION),
    ignore_paths: list[str] = typer.Option([], "--ignore", "-i", help=HELP_I_OPTION),
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

    # Determine target SCRUM_STATUS. by default, from Backlog up
    # i.e., everything that has an estimated time (by default an hour)
    if icebox is True:
        target_scrum_status = [SCRUM_STATUS.ICEBOX]
    elif current is True:
        target_scrum_status = [
            SCRUM_STATUS.WAITING,
            SCRUM_STATUS.DOING,
            SCRUM_STATUS.CURRENT,
        ]
    else:
        target_scrum_status = [
            SCRUM_STATUS.WAITING,
            SCRUM_STATUS.DOING,
            SCRUM_STATUS.CURRENT,
            SCRUM_STATUS.BACKLOG,
        ]

    # Get graphs in processed paths
    graphs_paths_found: list[str] = get_graphs(paths)

    # Parse blocks in graphs, getting the ones with clocks or with the target
    # SCRUM_STATUS
    blocks_parsed = parse_graph_group(
        graphs_paths_found,
        filter=lambda x: (x.scrum_status in target_scrum_status) or (len(x.clocks) > 0),
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
    blocks["work_time"] = blocks["block"].apply(
        lambda x: x.total_clocked_time.total_seconds() / 3600.0
    )

    # Graph name (for sorting)
    blocks["graph_name"] = blocks["graph"].apply(lambda x: x.name)

    # Highest priority
    blocks["h_priority"] = blocks["block"].apply(lambda x: x.highest_priority)

    # Projected time
    blocks["estimated_time"] = blocks["block"].apply(lambda x: x.scrum_time)

    # Remaining time
    blocks["left_time"] = blocks.apply(
        lambda x: max(0, (x["estimated_time"] - x["work_time"])), axis=1
    )

    # Check for condensed or detailed block view
    if show_blocks is True:
        # Show blocks
        # Just sort, everything else is done
        blocks.sort_values(
            by=["scrum_status_value", "h_priority", "graph_name", "estimated_time"],
            inplace=True,
            ascending=[False, True, True, False],
        )
    else:
        # Condensed view, group by graph and status
        blocks = (
            blocks.groupby(["graph_name", "scrum_status_value", "scrum_status_name"])
            .agg(
                {
                    "block": "count",
                    "work_time": "sum",
                    "estimated_time": "sum",
                    "left_time": "sum",
                }
            )
            .reset_index()
        )

        # Sort
        blocks.sort_values(
            by=["scrum_status_value", "graph_name", "estimated_time"],
            inplace=True,
            ascending=[False, True, False],
        )

    # wt_et of completiness
    blocks["wt_et"] = blocks.apply(
        lambda row: row["work_time"] / row["estimated_time"]
        if row["estimated_time"] > 0
        else 0,
        axis=1,
    )

    # Data visualization
    console = Console()

    # Condensed versus block view
    if show_blocks is True:
        # Block view
        table = Table(
            title="SCRUM by Blocks",
            title_style=STYLE_TABLE_NAME,
            header_style=STYLE_TABLE_HEADER,
            box=box.SIMPLE_HEAD,
        )
        table.add_column("Graph", justify="left", max_width=COLUMN_WIDTH_GRAPH_NAME)
        table.add_column("Page", justify="left", max_width=COLUMN_WIDTH_PAGE_NAME)
        table.add_column("Block", justify="left")
        table.add_column("Status", justify="center")
        table.add_column("P", justify="center")
        table.add_column("ET", justify="center")
        table.add_column("WT", justify="center")
        table.add_column("LT", justify="center")
        table.add_column("WT/ET", justify="center")
    else:
        # Condensed view
        table = Table(
            title="SCRUM by Graphs",
            title_style=STYLE_TABLE_NAME,
            header_style=STYLE_TABLE_HEADER,
            box=box.SIMPLE_HEAD,
        )
        table.add_column("Graph", justify="left")
        table.add_column("Status", justify="center")
        table.add_column("# Blocks", justify="center")
        table.add_column("ET", justify="center")
        table.add_column("WT", justify="center")
        table.add_column("LT", justify="center")
        table.add_column("WT/ET", justify="center")

    # An index to shade rows
    i: int = 1

    # Iterate rows
    # Once again, depends on the type of view
    for index, row in blocks.iterrows():
        # Common styles for both views
        if row["scrum_status_name"] == "WAITING":
            style = STYLE_ROW_SCRUM_WAITING
        elif row["scrum_status_name"] == "DOING":
            style = STYLE_ROW_SCRUM_DOING
        elif row["scrum_status_name"] == "CURRENT":
            style = STYLE_ROW_SCRUM_CURRENT
        elif row["scrum_status_name"] == "BACKLOG":
            style = STYLE_ROW_SCRUM_BACKLOG
        else:
            style = STYLE_ROW_NORMAL

        # Add shade for alternate rows
        if i % 2 == 0:
            style += STYLE_ROW_NORMAL_SHADE_MODIFIER

        wt_et_highlighted: Text = Text(
            str(
                round(
                    row["wt_et"],
                    1,
                )
            ),
            style=STYLE_TEXT_HIGHLIGHT if row["wt_et"] > 1.0 else style,
        )

        if show_blocks is True:
            # Block view
            priority_highlighted: Text = Text(
                str(row["h_priority"]) if row["h_priority"] is not None else "",
                style=STYLE_TEXT_HIGHLIGHT if row["h_priority"] == "A" else style,
            )

            table.add_row(
                row["graph_name"],
                row["page"].title,
                Text(row["block"].clean_title),
                row["scrum_status_name"],
                priority_highlighted,
                str(row["estimated_time"]),
                str(round(row["work_time"], 1)),
                str(round(row["left_time"], 1)),
                wt_et_highlighted,
                style=style,
            )

        else:
            # Condensed view

            table.add_row(
                row["graph_name"],
                row["scrum_status_name"],
                str(row["block"]),
                str(row["estimated_time"]),
                str(round(row["work_time"], 1)),
                str(round(row["left_time"], 1)),
                wt_et_highlighted,
                style=style,
            )

        i += 1

    # Highlight the total % if greater than 1
    total_highlighted: Text = Text(
        str(round(blocks["work_time"].sum() / blocks["estimated_time"].sum(), 1)),
        style=STYLE_TEXT_HIGHLIGHT
        if round(blocks["work_time"].sum() / blocks["estimated_time"].sum(), 1) > 1.0
        else STYLE_TOTAL,
    )

    # Total row, view dependant
    if show_blocks is True:
        # Block view

        table.add_row(
            "TOTAL",
            "",
            str(blocks.shape[0]),
            "",
            "",
            str(blocks["estimated_time"].sum()),
            str(round(blocks["work_time"].sum(), 1)),
            str(round(blocks["left_time"].sum(), 1)),
            total_highlighted,
            style=STYLE_TOTAL,
        )

    else:
        # Condensed view
        table.add_row(
            "TOTAL",
            "",
            str(blocks["block"].sum()),
            str(blocks["estimated_time"].sum()),
            str(round(blocks["work_time"].sum(), 1)),
            str(round(blocks["left_time"].sum(), 1)),
            total_highlighted,
            style=STYLE_TOTAL,
        )

    console.print(table)

    print(
        "  P: Priority, ET: estimated time, WT: work time , LT: left time, WT/ET: completiness"
    )

    print()

    table = Table(show_header=False, show_lines=False, show_edge=False, pad_edge=False)

    table.add_row(
        f"  Mean speed in the last [red bold]{weeks}[/] weeks",
        f"[red bold]{round(mean_speed, 1)}[/]",
    )

    table.add_row(
        "  # weeks to complete all LT",
        f"[red bold]{round(blocks['left_time'].sum() / mean_speed, 1)}[/]",
    )

    console.print(table)

    print()