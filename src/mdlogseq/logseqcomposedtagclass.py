from marko import inline
from .processmultitags import processMultiTags

class LogseqComposedTag(inline.InlineElement):

  pattern = r'#\[\[*(.+?)\]\]'
  parse_children = True
  priority = 7

  def __init__(self, match):
    self.target = processMultiTags(match.group(1))
