import sys

import arrow
import pandas as pd
import typer
from lib.constants import (
    STYLE_ROW_NORMAL,
    STYLE_SHADE,
    STYLE_TABLE_HEADER,
    STYLE_TABLE_NAME,
    STYLE_TOTAL,
)
from lib.libmlkgraph import (
    get_graphs,
    parse_graph_group,
    process_p_g_i_graph_paths,
)
from pylogseq import Clock
from rich import box
from rich import print as pprint
from rich.console import Console
from rich.table import Table


# ----------------------
#
# Command to check current week hours allocation between graphs.
#
# ----------------------
def sprint(
    show_blocks: bool = typer.Option(
        False, "--blocks", "-b", help="Show time for blocks instead of graphs"
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

    # Calculate Arrow spans for the last week
    today = arrow.now()

    span = today.span("week")
    clock = Clock(span[0].naive, span[1].naive)

    # Parse blocks in graphs
    blocks_parsed = parse_graph_group(
        graphs_paths_found,
        lambda x: x.total_intersection_time(clock).total_seconds() > 0,
    )

    # Bail out if no blocks found
    if len(blocks_parsed) == 0:
        pprint(
            f"[red bold]No blocks found in the given time span: {span[0].naive.strftime('%Y-%m-%d')} / {span[1].naive.strftime('%Y-%m-%d')}[/]"
        )
        sys.exit(0)

    # Transform blocks into a DataFrame
    blocks: pd.DataFrame = pd.DataFrame(blocks_parsed)

    # Process dataframe columns
    blocks["graph"] = blocks["graph"].apply(lambda x: x.name)
    blocks["page"] = blocks["page"].apply(lambda x: x.title)
    blocks["block_name"] = blocks["block"].apply(lambda x: x.clean_title)

    # TODO: Esto será útil en otro comando
    # blocks["programmed_time"] = blocks["block"].apply(lambda x: x.scrum_time)

    # Calculate the total time for the week
    blocks["total_time"] = blocks["block"].apply(
        lambda x: x.total_intersection_time(clock).total_seconds() / 3600.0
    )

    # TODO: Útil para otro comando
    # blocks["completeness"] = blocks.apply(
    #     lambda x: x["total_time"] / x["programmed_time"]
    #     if x["programmed_time"] > 0
    #     else npnan,
    #     axis=1,
    # )

    if show_blocks is True:
        blocks = (
            blocks[["graph", "block_name", "total_time"]]
            .groupby(["graph", "block_name"])
            .sum()
        )
    else:
        blocks = blocks[["graph", "total_time"]].groupby("graph").sum()

    print()

    # Sum total hours
    total_hours: float = blocks["total_time"].sum()

    # Data visualization
    console = Console()

    # Table definition
    # Number of columns depends on block or graph view
    table = Table(
        title=f"Tiempo pasado en {'bloques' if show_blocks is True else 'grafos'} esta semana",
        title_style=STYLE_TABLE_NAME,
        header_style=STYLE_TABLE_HEADER,
        box=box.SIMPLE_HEAD,
    )

    if show_blocks is True:
        table.add_column("Grafo", justify="left")
        table.add_column("Bloque", justify="left")
        table.add_column("Horas", justify="center")
        table.add_column("%", justify="center")
    else:
        table.add_column("Grafo", justify="left")
        table.add_column("Horas", justify="center")
        table.add_column("%", justify="center")

    # Ordenamos por tiempo
    blocks.sort_values("total_time", ascending=False, inplace=True)

    # An index to shade rows
    i: int = 0

    # Iterate rows
    for index, row in blocks.iterrows():
        style = STYLE_ROW_NORMAL

        # Add shade for alternate rows
        if (i + 1) % 4 == 0:
            style += STYLE_SHADE

        if show_blocks is True:
            table.add_row(
                str(index[0]),  # type: ignore
                str(index[1]),  # type: ignore
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
            str(round(total_hours, 1)),
            "-",
            style=STYLE_TOTAL,
        )
    else:
        table.add_row(
            "TOTAL",
            str(round(total_hours, 1)),
            "-",
            style=STYLE_TOTAL,
        )

    console.print(table)

    table = Table(show_header=False, show_lines=False, show_edge=False, pad_edge=False)

    # table.add_row("Horas prorrateadas (5 días / semana)", justify="left")

    table.add_row(
        "Horas diarias prorrateadas (5 días / semana)", str(round(total_hours / 5.0, 1))
    )

    table.add_row(
        "Horas diarias hasta ahora", str(round(total_hours / today.isoweekday(), 1))
    )

    console.print(table)

    print()
