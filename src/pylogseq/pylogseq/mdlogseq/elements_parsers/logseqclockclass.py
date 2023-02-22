from marko import inline
from datetime import datetime
from ..exceptions.errorclock import ErrorClock
import re

# --------------------------------------
#
# Parses a CLOCK line in LOGBOOK sections.
#
# --------------------------------------
class LogseqClock(inline.InlineElement):
  """Parses a CLOCK line in LOGBOOK sections.

  The parsing reports a target with the following items:

    startDate                  Start date
    startDay                   Start day of the week
    startHour                  Start hour
    start                      Start as timestamp

    endDate                    Ending date
    endDay                     Ending day of the week
    endHour                    Ending hour
    end                        Ending as timestamp

    elapsedTime                Elapsed time as stated in CLOCK
    calculatedElapsedTime      Real calculated elapsed time from timestamps

  Raises:
      ErrorClock: raises in several scenarios.
  """

  # Pattern to match.
  pattern: str = r"\s*(CLOCK:.*\n?)"
  """The pattern to match."""

  # Don't parse children, there is nothing interesting inside.
  parse_children: bool = False
  """Don't parse children, there is nothing interesting inside."""

  # Priority.
  priority: int = 10
  """Priority."""

  # --------------------------------------
  #
  # Constructor.
  #
  # --------------------------------------
  def __init__(self, match: re.Match):
    """Constructor.

    Args:
        match (re.Match): The matching results.

    Raises:
        ErrorClock: Raises in several scenarios.
    """
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
        raise ErrorClock("CLOCK error: start time bigger than end time %s > %s" % (
            "%s %s %s" % (m.group(2), m.group(3), m.group(4)),
            "%s %s %s" % (m.group(5), m.group(6), m.group(7))
          ))
      else:
        # Everything ok, report parsed result
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
