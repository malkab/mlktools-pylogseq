from marko import inline
from datetime import datetime
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
      self.target = {
        "errorInCLOCK": "unparseableCLOCK",
        "CLOCK": str
      }

    else:
      # Store the start and end time as timestamps
      try:
        start = datetime.strptime("%s %s" % \
          (m.group(2), m.group(4)), '%Y-%m-%d %H:%M:%S')

      except:
        self.target = {
          "errorInCLOCK": "unparseableTimestamp",
          "timestamp": "%s %s" % (m.group(2), m.group(4))
        }

        return

      try:
        end = datetime.strptime("%s %s" % \
          (m.group(5), m.group(7)), '%Y-%m-%d %H:%M:%S')

      except:
        self.target = {
          "errorInCLOCK": "unparseableTimestamp",
          "timestamp": "%s %s" % (m.group(5), m.group(7))
        }

        return

      # Check different days clocking
      if m.group(2) != m.group(5):
        self.target = {
          "errorInCLOCK": "differentDays",
          "startDate": m.group(2),
          "endDate": m.group(5)
        }

      elif end<start:
        self.target = {
          "errorInCLOCK": "startBiggerThanEnd",
          "startDate": m.group(2),
          "startDay": m.group(3),
          "startHour": m.group(4),
          "start": start,
          "endDate": m.group(5),
          "endDay": m.group(6),
          "endHour": m.group(7),
          "end": end,
        }

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
