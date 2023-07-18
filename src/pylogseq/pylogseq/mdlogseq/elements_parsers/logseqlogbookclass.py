from marko import inline

# TODO: DOCUMENT

class LogseqLogBook(inline.InlineElement):

  pattern = r'(:LOGBOOK:)'
  parse_children = False
  priority = 6

  def __init__(self, match):
    self.target = match.group(0)
