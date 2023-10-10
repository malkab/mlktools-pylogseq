from marko import inline
from .process_multi_tags import process_multi_tags

# TODO: DOCUMENT

class LogseqComposedTag(inline.InlineElement):

  pattern = r'#\[\[*(.+?)\]\]'
  parse_children = True
  priority = 7

  def __init__(self, match):
    self.target = process_multi_tags(match.group(1))
