from marko import inline

class LogseqDone(inline.InlineElement):

  pattern = r'(DONE)'
  parse_children = False
  priority = 6

  def __init__(self, match):
    self.target = match.group(0)
