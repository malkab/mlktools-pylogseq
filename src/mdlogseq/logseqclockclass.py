from marko import inline
import re

class LogseqClock(inline.InlineElement):

  pattern = r"\s*(CLOCK:.*\n?)"
  parse_children = False
  priority = 10

  def __init__(self, match):
    str = match.group(1)
    pattern = r"(\s?CLOCK:)\s\[(.*)\s(.*)\s(.*)\]--\[(.*)\s(.*)\s(.*)\] =>  (.*)\n"

    m = re.match(pattern, str)

    print("D: ", match)

    if m == None:
      self.target = { "errorInCLOCK": str }
    else:
      self.target = {
        "startDate": m.group(2),
        "startDay": m.group(3),
        "startHour": m.group(4),

        "endDate": m.group(5),
        "endDay": m.group(6),
        "endHour": m.group(7),

        "elapsedTime": m.group(8)
      }
