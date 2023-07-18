from marko import inline
from re import Match

# TODO: DOCUMENT

# --------------------------------------
#
# Parser element: Logseq priority
#
# --------------------------------------
class LogseqPriority(inline.InlineElement):
  """Parser element for Logseq priority."""

  # --------------------------------------
  #
  # The pattern to match.
  #
  # --------------------------------------
  pattern: str = r'\[\#(A|B|C)\]'
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
  priority = 6
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
    self.target = match.group(1)
