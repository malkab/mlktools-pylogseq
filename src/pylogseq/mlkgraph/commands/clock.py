import datetime
import sys

import arrow
import pandas as pd
import typer
from pylogseq.mlkgraph.lib.constants import (
    COLUMN_WIDTH_GRAPH_NAME,
    HELP_B_OPTION,
    HELP_G_OPTION,
    HELP_I_OPTION,
    HELP_P_OPTION,
    STYLE_ROW_NORMAL,
    STYLE_ROW_NORMAL_SHADE,
    STYLE_TABLE_HEADER,
    STYLE_TABLE_NAME,
    STYLE_TOTAL,
)
from pylogseq.mlkgraph.lib.libmlkgraph import (
    get_graphs,
    parse_graph_group,
    process_p_g_i_graph_paths,
)
from pylogseq.pylogseq import Clock
from rich import box
from rich import print as pprint
from rich.console import Console
from rich.table import Table


# ----------------------
#
# Command to check current week hours allocation between graphs.
#
# ----------------------
def clock(
    show_blocks: bool = typer.Option(False, "--blocks", "-b", help=HELP_B_OPTION),
    span_start: str = typer.Option(
        "", "--start", "-s", help="Start date for the span."
    ),
    span_end: str = typer.Option("", "--end", "-e", help="End date for the span."),
    shift: str = typer.Option("", "--shift", "-f", help="Span time segmentation."),
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

    # If span_start, try to parse the date. If not, use the current week
    if span_start != "":
        span_start_date = arrow.get(span_start, "YYYY-MM-DD").naive
    else:
        span_start_date: datetime.datetime = arrow.now().floor("week").naive

    # Same with end
    if span_end != "":
        span_end_date: datetime.datetime = arrow.get(span_end, "YYYY-MM-DD").naive
    else:
        span_end_date: datetime.datetime = arrow.now().naive

    # Table title time particle
    time_particle: str = ""

    # If there is a shift, process it, takes precedence over start and end
    if shift != "":
        # Split the shift in number and unit
        shift_split: list[str] = shift.split(" ")

        # Try to find predefined shifts
        if len(shift_split) == 1:
            if shift_split[0] == "today":
                shift_split = ["0", "days"]
                time_particle = "today"
            elif shift_split[0] == "yesterday":
                shift_split = ["1", "days"]
                time_particle = "yesterday"
            elif shift_split[0] == "week":
                shift_split = ["0", "weeks"]
                time_particle = "this week"
            elif shift_split[0] == "month":
                shift_split = ["0", "months"]
                time_particle = "this month"
            elif shift_split[0] == "year":
                shift_split = ["0", "years"]
                time_particle = "this year"
        elif len(shift_split) == 2:
            if shift_split[0] == "last":
                if shift_split[1] == "week":
                    shift_split = ["1", "weeks"]
                    time_particle = "last week"
                elif shift_split[1] == "month":
                    shift_split = ["1", "months"]
                    time_particle = "last month"
                elif shift_split[1] == "year":
                    shift_split = ["1", "years"]
                    time_particle = "last year"

        # Bail out if the shift is not well formed
        if len(shift_split) != 2:
            shift_error(shift)

        # Extract number and unit
        shift_number: int = 0
        shift_unit: str = ""

        try:
            shift_number = int(shift_split[0])
            shift_unit = shift_split[1]
        except Exception:
            shift_error(shift)

        # Try to calculate the shift
        try:
            shift_date = arrow.now().shift(**{shift_unit: -shift_number})

            # Generic time particle for title if still not defined
            time_particle = (
                f"{shift_number} {shift_unit} ago"
                if time_particle == ""
                else time_particle
            )
        except Exception:
            shift_error(shift)

        span_start_date = shift_date.floor(shift_unit).naive  # type: ignore

        # If the shift is a current time span (year, month, week, today), the end is now
        # If not, it is the end of the indicated time span
        if shift_split[0] == "0":
            span_end_date = datetime.datetime = arrow.now().naive
        else:
            span_end_date = shift_date.ceil(shift_unit).naive  # type: ignore

    # Time particle for the title if there are no options
    if span_start == "" and span_end == "" and shift == "":
        time_particle = "to this point of the week"

    clock = Clock(span_start_date, span_end_date)

    if clock is None:
        pprint("[red bold]No clock defined[/]")
        sys.exit(0)

    # Parse blocks in graphs
    blocks_parsed = parse_graph_group(
        graphs_paths_found,
        lambda x: x.total_intersection_time(clock).total_seconds() > 0,
    )

    # Bail out if no blocks found
    if len(blocks_parsed) == 0:
        pprint(
            f"[red bold]No blocks found in the given time span: {span_start_date.strftime('%Y-%m-%d')} / {span_end_date.strftime('%Y-%m-%d')}[/]"
        )
        sys.exit(0)

    # Transform blocks into a DataFrame
    blocks: pd.DataFrame = pd.DataFrame(blocks_parsed, index=None)

    # Process dataframe columns
    blocks["graph"] = blocks["graph"].apply(lambda x: x.name)
    blocks["page"] = blocks["page"].apply(lambda x: x.title)
    blocks["block_name"] = blocks["block"].apply(lambda x: x.clean_title)

    # Calculate the total time for the week
    blocks["total_time"] = blocks["block"].apply(
        lambda x: x.total_intersection_time(clock).total_seconds() / 3600.0
    )

    if show_blocks is True:
        blocks = (
            blocks[["graph", "page", "block_name", "total_time"]]
            .groupby(["graph", "page", "block_name"])  # type: ignore
            .sum()
        )
    else:
        blocks = blocks[["graph", "total_time"]].groupby("graph").sum()  # type: ignore

    print()

    # Sum total hours
    total_hours: float = blocks["total_time"].sum()

    # Data visualization
    console = Console()

    # Title
    if time_particle != "":
        table_title = f"Time spent on {'blocks' if show_blocks is True else 'graphs'} {time_particle}"
    else:
        table_title = f"Time spent on {'blocks' if show_blocks is True else 'graphs'} in period {span_start_date.strftime('%Y-%m-%d')} / {span_end_date.strftime('%Y-%m-%d')}"

    # Table definition
    # Number of columns depends on block or graph view
    table = Table(
        title=table_title,
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )

    if show_blocks is True:
        table.add_column("Graph", justify="left", max_width=COLUMN_WIDTH_GRAPH_NAME)
        table.add_column("Page", justify="left", max_width=COLUMN_WIDTH_GRAPH_NAME)
        table.add_column("Block", justify="left")
        table.add_column("Hours", justify="center")
        table.add_column("%", justify="center")
    else:
        table.add_column("Graph", justify="left")
        table.add_column("Hours", justify="center")
        table.add_column("%", justify="center")

    # Ordenamos por tiempo
    blocks.sort_values("total_time", ascending=False, inplace=True)

    # An index to shade rows
    i: int = 1

    # Iterate rows
    for index, row in blocks.iterrows():
        # Shading alternate rows
        style = STYLE_ROW_NORMAL if i % 2 != 0 else STYLE_ROW_NORMAL_SHADE

        if show_blocks is True:
            table.add_row(
                str(index[0]),  # type: ignore
                str(index[1]),  # type: ignore
                str(index[2]),  # type: ignore
                str(round(row["total_time"], 1)),
                str(round(row["total_time"] / total_hours, 1)),
                style=style,
            )
        else:
            table.add_row(
                index,  # type: ignore
                str(round(row["total_time"], 1)),
                str(round(row["total_time"] / total_hours, 1)),
                style=style,
            )

        i += 1

    # Total row
    if show_blocks is True:
        table.add_row(
            "TOTAL",
            "",
            "",
            str(round(total_hours, 1)),
            "",
            style=STYLE_TOTAL,
        )
    else:
        table.add_row(
            "TOTAL",
            str(round(total_hours, 1)),
            "",
            style=STYLE_TOTAL,
        )

    console.print(table)

    table = Table(show_header=False, show_lines=False, show_edge=False, pad_edge=False)

    # Calculate working days in time span
    # Initialize a counter for the non-weekend days
    non_weekend_days = 0

    # Iterate over the days in the time span
    for day in arrow.Arrow.range("day", span_start_date, span_end_date):
        # If the day is not a weekend day, increment the counter
        if day.format("d") not in ["6", "7"]:
            non_weekend_days += 1

    table.add_row("  Workdays in time span", f"[red bold]{str(non_weekend_days)}[/]")
    table.add_row(
        "  Daily hours in time span",
        str(f"[red bold]{round(total_hours / non_weekend_days, 1)}[/]"),
    )

    console.print(table)

    print()


# ----------------------
#
# Displays the shift error.
#
# ----------------------
def shift_error(shift: str):
    pprint(f"[red bold]Invalid shift '{shift}'[/]")
    pprint(
        "[red bold]Specific valid units are: 'year', 'month', 'week', 'today', 'last year', 'last month', 'last week', 'yesterday' (week is default if no options are provided)[/]"
    )
    pprint(
        "[red bold]Generic valid units are: 'x years', 'x months', 'x weeks', 'x days'[/]"
    )
    sys.exit(0)
