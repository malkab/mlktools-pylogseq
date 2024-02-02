# ----------------------
#
# Constants
#
# ----------------------
STYLE_ROW_HIGHLIGHT_A = "black on orange1"
STYLE_ROW_HIGHLIGHT_A_SHADE = "black on dark_orange"
STYLE_ROW_HIGHLIGHT_B = "black on orange3"
STYLE_ROW_HIGHLIGHT_B_SHADE = "black on dark_orange3"
STYLE_ROW_NORMAL = "black"
STYLE_ROW_NORMAL_SHADE = "black on grey85"
STYLE_ROW_NORMAL_SHADE_MODIFIER = " on grey85"
STYLE_ROW_SCRUM_BACKLOG = "blue"
STYLE_ROW_SCRUM_CURRENT = "green"
STYLE_ROW_SCRUM_DOING = "red"
STYLE_ROW_SCRUM_WAITING = "yellow"
STYLE_ROW_WARNING = "bold bright_white on bright_red"
STYLE_ROW_WARNING_SHADE = "bold bright_white on red"
STYLE_TABLE_HEADER = "blue bold"
STYLE_TABLE_NAME = "red bold"
STYLE_TEXT_HIGHLIGHT = "bright_white on red bold"
STYLE_TOTAL = "red bold on gold1"

# Tamaños de las columnas
COLUMN_WIDTH_GRAPH_NAME = 30
COLUMN_WIDTH_PAGE_NAME = 25

# Help for common options
HELP_P_OPTION = "Profiles to apply, in order, comma-separated. Multiple -p allowed."
HELP_G_OPTION = (
    "Graphs to analyze, comma-separated. Multiple -g allowed. Globs can be provided."
)
HELP_I_OPTION = "Graph paths to ignore, comma-separated. Multiple -i allowed. Globs can be provided."
HELP_B_OPTION = "Show blocks instead of graphs."
HELP_PGI_GENERAL = """\n
Globs in -pgi options must be quoted to avoid shell expansion.

If no -pgi options are given, the command uses the current folder as the starting point to look for graphs.
"""
