import sys

import pandas as pd
import typer
from lib.constants import STYLE_TABLE_HEADER, STYLE_TABLE_NAME
from lib.libmlkgraph import (
    get_graphs,
    process_p_g_i_graph_paths,
)
from lib.profiles import Profiles
from rich import box
from rich import print as pprint
from rich.console import Console
from rich.table import Table


# ----------------------
#
# profiles command
#
# ----------------------
def profiles(
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Debug mode, showing the results of processing of globs.",
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
    # List profiles if no -pgi option is given
    if (
        len(selected_profiles) == 0
        and len(graphs_paths) == 0
        and len(ignore_paths) == 0
    ):
        # Data visualization
        console = Console()

        profiles: Profiles = Profiles()

        profiles.read_profiles()

        df: pd.DataFrame = pd.DataFrame(profiles.profiles).T

        table = Table(
            title="Profiles",
            title_style=STYLE_TABLE_NAME,
            header_style=STYLE_TABLE_HEADER,
            box=box.SIMPLE_HEAD,
        )
        table.add_column("ID", justify="left")
        table.add_column("Description", justify="left")

        # Sort by index (ID of the profile)
        df.sort_index(inplace=True)

        # Check if there are profiles in the DataFrame
        if df.shape[0] > 0:
            # Index for shading
            for k, v in df.iterrows():
                table.add_row(str(k), v["description"])

            print()

            console.print(table)

        else:
            pprint("[red bold]No profiles found in .mlkgraphprofiles files\n[/]")

    # Tests graphs resolved if pgi options are given
    else:
        # Process pgi options
        try:
            paths: list[str] = process_p_g_i_graph_paths(
                selected_profiles, graphs_paths, ignore_paths, debug
            )
        except Exception as e:
            pprint(f"[red bold]{e}[/]")
            sys.exit(1)

        graphs = get_graphs(paths)

        # Check if any graph path was resolved
        if len(graphs) == 0:
            pprint("[red bold]No graphs resolved[/]")
        else:
            for f in sorted(graphs):
                pprint(f"[green]{f}[/]")
