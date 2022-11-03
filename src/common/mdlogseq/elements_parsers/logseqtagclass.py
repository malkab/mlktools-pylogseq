from marko import inline
from .processmultitags import processMultiTags

class LogseqTag(inline.InlineElement):

  pattern = r'#(\b.+?\s)'
  parse_children = True
  priority = 6

  def __init__(self, match):
    self.target = processMultiTags(match.group(1))
