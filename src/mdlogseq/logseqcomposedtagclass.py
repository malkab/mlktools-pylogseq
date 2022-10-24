from marko import inline

class LogseqComposedTag(inline.InlineElement):

  pattern = r'\#\[\[ *(.+?) *\]\]'
  parse_children = True

  def __init__(self, match):
    self.target = match.group(2)
