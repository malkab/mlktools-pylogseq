from marko import inline
from .processmultitags import processMultiTags

class LogseqSquareTag(inline.InlineElement):

  pattern = r"\[\[(\b.+?\b)\]\]"
  parse_children = True
  priority = 6

  def __init__(self, match):
    self.target = processMultiTags(match.group(1))
