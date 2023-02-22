from marko import inline
from .processmultitags import processMultiTags
from re import Match

class LogseqTag(inline.InlineElement):
  """Parser element for Logseq simple #A tag."""

  pattern = r'#([A-Za-z0-9/]+)'
  """The pattern to match."""

  parse_children = True
  """Don't parse child objects."""

  priority = 6
  """Priority."""

  def __init__(self, match: Match):
    """Constructor.

    Args:
        match (Match): The match from the pattern.
    """
    self.target = processMultiTags(match.group(1))
