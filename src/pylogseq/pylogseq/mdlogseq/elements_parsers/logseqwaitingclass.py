from marko import inline
from re import Match

# TODO: DOCUMENT


class LogseqWaiting(inline.InlineElement):
    """Parser element for Logseq WAITING mark."""

    pattern: str = r"^(WAITING)"
    """The pattern to match."""

    parse_children: bool = False
    """Don't parse child objects."""

    priority: int = 6
    """Priority."""

    def __init__(self, match: Match):
        """Constructor.

        Args:
            match (Match): The match from the pattern.
        """
        self.target = match.group(0)
