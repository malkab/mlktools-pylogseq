from marko import inline
from re import Match

# --------------------------------------
#
# Parser element: Logseq DONE
#
# --------------------------------------
class LogseqDone(inline.InlineElement):
  """Parser element for Logseq DONE mark."""

  # --------------------------------------
  #
  # The pattern to match.
  #
  # --------------------------------------
  pattern: str = r'^(DONE)'
  """The pattern to match."""

  # --------------------------------------
  #
  # Don't parse children.
  #
  # --------------------------------------
  parse_children: bool = False
  """Don't parse child objects."""

  # --------------------------------------
  #
  # Priority.
  #
  # --------------------------------------
  priority: int = 6
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
    self.target = match.group(0)
