import os
import fnmatch
from .page import Page

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
        self.pages_file_name = []
        self.pages = []

    # ----------------------------------
    #
    # Get all .md files in graph.
    #
    # ----------------------------------
    def get_md_pages(self):
        """Get all .md files in graph folder tree.

        Returns:
            list: A list of all .md files in graph.
        """
        # Check if the path exists
        if not os.path.exists(self.path):
            raise Exception(f"Graph path {self.path} does not exist.")

        for dirpath, dirnames, filenames in os.walk(self.path):
            page_file_n = fnmatch.filter(filenames, "*.md")

            for fn in page_file_n:
                self.pages_file_name.append(os.path.join(dirpath, fn))

    # ----------------------------------
    #
    # Read all pages in graph.
    #
    # ----------------------------------
    def read_pages(self):
        """Read all pages in graph.
        """
        for p in self.pages_file_name:
            page = Page()
            page.read_page_file(p)
            page.parse_markdown()
            self.pages.append(page)
            yield page
