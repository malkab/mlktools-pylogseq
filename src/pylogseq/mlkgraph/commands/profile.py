import sys

import pandas as pd
import typer
from pylogseq.mlkgraph.lib.constants import (
    HELP_G_OPTION,
    HELP_I_OPTION,
    HELP_P_OPTION,
    STYLE_ROW_NORMAL,
    STYLE_ROW_NORMAL_SHADE,
    STYLE_TABLE_HEADER,
    STYLE_TABLE_NAME,
)
from pylogseq.mlkgraph.lib.libmlkgraph import (
    get_graphs,
    process_p_g_i_graph_paths,
)
from pylogseq.mlkgraph.lib.profiles import Profiles
from rich import box
from rich import print as pprint
from rich.console import Console
from rich.table import Table


# ----------------------
#
# profiles command
#
# ----------------------
def profile(
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
            # An index to shade rows
            i: int = 1

            # Index for shading
            for k, v in df.iterrows():
                # Base style
                style = STYLE_ROW_NORMAL if i % 2 != 0 else STYLE_ROW_NORMAL_SHADE

                table.add_row(str(k), v["description"], style=style)

                i += 1

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
