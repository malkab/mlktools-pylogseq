from marko import inline
from re import Match

class LogseqNow(inline.InlineElement):
  """Parser element for Logseq NOW mark."""

  pattern: str = r'^(NOW)'
  """The pattern to match."""


  parse_children: bool = False
  """Don't parse child objects."""


  priority: int = 6
  """Priority."""


  def __init__(self, match: Match):
    """Constructor.

    Args:
        match (Match): The match from the pattern.
    """
    self.target = match.group(0)
