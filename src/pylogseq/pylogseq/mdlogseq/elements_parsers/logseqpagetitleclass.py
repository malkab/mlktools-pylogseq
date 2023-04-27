from marko import inline
from re import Match

class LogseqPageTitle(inline.InlineElement):

  pattern = r'title::(.*)'
  parse_children = False
  priority = 10

  def __init__(self, match: Match):
    self.target = match.group(1).strip()
