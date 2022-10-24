from marko import inline

class LogseqClock(inline.InlineElement):

  pattern = r"(\s?CLOCK:)\s\[(.*)\s(.*)\s(.*)\]--\[(.*)\s(.*)\s(.*)\] =>  (.*)\n"
  parse_children = False
  priority = 3

  def __init__(self, match):
    self.target = [ match.group(1), match.group(2), match.group(3), match.group(4) ]
