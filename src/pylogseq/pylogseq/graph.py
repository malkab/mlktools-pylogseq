"""Represents a Logseq Graph.
"""

class Graph():
    """Represents a Logseq Graph.

    Attributes:
        likes_spam:
            A boolean indicating if we like SPAM or not.
        eggs:
            An integer count of the eggs we have laid.
    """

    def __init__(self, path: str):
        """Constructor.

        Args:
            path (str): The path to the graph's folder.
        """
        self.path = path
