import os
import fnmatch
from .page import Page
from .block import Block

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
        self.path = path.rstrip("/")
        self.pages_file_name = []
        self.pages = []
        self.title = os.path.split(self.path)[-1]

    # ----------------------------------
    #
    # Get all .md files in graph.
    #
    # ----------------------------------
    def get_pages(self):
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
                # Filter all stuff at logseq/bak and at logseq/.recycle
                if "logseq/bak" not in dirpath and "logseq/.recycle" not in dirpath:
                    self.pages_file_name.append(os.path.join(dirpath, fn))

    # ----------------------------------
    #
    # Read all pages in graph.
    #
    # ----------------------------------
    def parse(self) -> None:
        """Read all pages in graph.
        """
        for p in self.pages_file_name:
            page = Page()
            page.read_page_file(p)
            page.parse()
            page.graph = self
            self.pages.append(page)
            yield page

    # ----------------------------------
    #
    # Get all blocks in graph.
    #
    # ----------------------------------
    def get_all_blocks(self) -> list[Block]:
        """Get all blocks in graph.

        Returns:
            list[Block]: A list of all blocks in graph.
        """
        blocks = []

        for page in self.pages:
            blocks.extend(page.blocks)

        return blocks
