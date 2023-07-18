from marko import inline
from pylogseq.mdlogseq.elements_parsers.processmultitags import processMultiTags

# TODO: DOCUMENT

class LogseqComposedTag(inline.InlineElement):

  pattern = r'#\[\[*(.+?)\]\]'
  parse_children = True
  priority = 7

  def __init__(self, match):
    self.target = processMultiTags(match.group(1))
