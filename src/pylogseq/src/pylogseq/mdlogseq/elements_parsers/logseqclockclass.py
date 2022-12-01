from marko import inline
from datetime import datetime
from ..exceptions.errorclock import ErrorClock
import re

class LogseqClock(inline.InlineElement):

  pattern = r"\s*(CLOCK:.*\n?)"
  parse_children = False
  priority = 10

  def __init__(self, match):
    str = match.group(1)
    pattern = r"(\s?CLOCK:)\s\[(.*)\s(.*)\s(.*)\]--\[(.*)\s(.*)\s(.*)\] =>  (.*)\n"

    m = re.match(pattern, str)

    if m == None:

      # Generic error
      raise ErrorClock(("CLOCK error: undefined error parsing %s" % str).strip("\n"))

    else:

      # Unparseable start time
      try:
        start = datetime.strptime("%s %s" %
          (m.group(2), m.group(4)), '%Y-%m-%d %H:%M:%S')

      except:
        raise ErrorClock("CLOCK error: unparseable start timestamp %s %s" %
          (m.group(2), m.group(4)))

      # Unparseable end time
      try:
        end = datetime.strptime("%s %s" % \
          (m.group(5), m.group(7)), '%Y-%m-%d %H:%M:%S')

      except:
        raise ErrorClock("CLOCK error: unparseable ending timestamp %s %s" %
          (m.group(5), m.group(7)))

      # Check different days clocking
      if m.group(2) != m.group(5):
        raise ErrorClock("CLOCK error: clocking in different days %s <> %s" %
          (m.group(2), m.group(5)))

      elif end<start:
        raise ErrorClock("ERROR! Start time bigger than end time %s > %s" % (
            "%s%s%s" % (m.group(2), m.group(3), m.group(4)),
            "%s%s%s" % (m.group(5), m.group(6), m.group(7))
          ))

      else:
        self.target = {
          "startDate": m.group(2),
          "startDay": m.group(3),
          "startHour": m.group(4),
          "start": start,

          "endDate": m.group(5),
          "endDay": m.group(6),
          "endHour": m.group(7),
          "end": end,

          "elapsedTime": m.group(8),
          "calculatedElapsedTime": end - start
        }
