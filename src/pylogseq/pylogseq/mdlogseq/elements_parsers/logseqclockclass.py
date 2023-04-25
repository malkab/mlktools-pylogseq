import sys
import os

# Add the parent directory of the current file to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from marko import inline
from datetime import datetime
from ..exceptions.errorclock import ErrorClock
from clock import Clock
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

        # Process
        if m != None:
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
            if end<start:
                raise ErrorClock("CLOCK error: start time bigger than end time %s > %s" % (
                    start, end))
            else:
                out: list[Clock] = []

                # Check if the 24h line has been crossed. If so, return
                # two time stamps, one for each day.
                if m.group(5) > m.group(2):
                    end_first_day = datetime.strptime("%s %s" %
                            (m.group(2), "23:59:59"), '%Y-%m-%d %H:%M:%S')

                    start_second_day = datetime.strptime("%s %s" %
                            (m.group(5), "00:00:01"), '%Y-%m-%d %H:%M:%S')

                    out.append(Clock(start, end_first_day))
                    out.append(Clock(start_second_day, end))

                else:
                    # Everything ok, report parsed result
                    out.append(Clock(start, end))

                self.target = out

        else:
            self.target = []
