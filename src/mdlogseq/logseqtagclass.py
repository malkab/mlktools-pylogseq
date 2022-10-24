from marko import inline

class LogseqTag(inline.InlineElement):

  pattern = r'#(\b.+?\b)'
  parse_children = True
  priority = 6

  def __init__(self, match):
    self.target = match.group(1)
