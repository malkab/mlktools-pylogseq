from marko import inline

# TODO: DOCUMENT

class LogseqEnd(inline.InlineElement):

  pattern = r'(:END:)'
  parse_children = False
  priority = 6

  def __init__(self, match):
    self.target = match.group(0)
