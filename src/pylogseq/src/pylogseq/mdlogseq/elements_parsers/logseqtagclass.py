from marko import inline
from .processmultitags import processMultiTags
from re import Match

# --------------------------------------
#
# Parser element: Logseg simple #A tag
#
# --------------------------------------
class LogseqTag(inline.InlineElement):
  """Parser element for Logseq simple #A tag."""

  # --------------------------------------
  #
  # The pattern to match.
  #
  # --------------------------------------
  pattern = r'#(.+?) '
  """The pattern to match."""

  # --------------------------------------
  #
  # Don't parse children.
  #
  # --------------------------------------
  parse_children = False
  """Don't parse child objects."""

  # --------------------------------------
  #
  # Priority.
  #
  # --------------------------------------
  priority = 2
  """Priority."""

  # --------------------------------------
  #
  # Constructor.
  #
  # --------------------------------------
  def __init__(self, match: Match):
    """Constructor.

    Args:
        match (Match): The match from the pattern.
    """
    self.target = processMultiTags(match.group(1))
