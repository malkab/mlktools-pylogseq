from marko import inline
from datetime import datetime
import re

# TODO: DOCUMENT

# --------------------------------------
#
# Parses an SCHEDULED section.
#
# --------------------------------------
class LogseqScheduled(inline.InlineElement):
    """Parses an SCHEDULED section.

    The parsing reports a target that is a datetime object.

    Raises:
        ErrorClock: raises in several scenarios.
    """

    # Pattern to match.
    pattern: str = r"\s*(SCHEDULED:.*\>)"
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
        pattern = r"(\s?SCHEDULED:)\s\<(.*)\>"

        # Get date data
        m = re.match(pattern, str)

        # Split the data
        date_data = m.group(2).split(" ")

        # Check if there is a time or not
        if len(date_data) == 2:
            self.target = datetime.strptime("%s" % (date_data[0]), '%Y-%m-%d')
        if len(date_data) == 3:
            self.target = datetime.strptime("%s %s" %
                (date_data[0], date_data[2]), '%Y-%m-%d %H:%M')
