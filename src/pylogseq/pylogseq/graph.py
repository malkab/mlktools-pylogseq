import os
import fnmatch
import hashlib
from .page import Page
from typing import Any
from .common import sanitize_path

"""Represents a Logseq Graph.
"""

class Graph():
    """Represents a Logseq Graph.

    TODO DOCUMENTATION

    Attributes:
        likes_spam:
            A boolean indicating if we like SPAM or not.
        eggs:
            An integer count of the eggs we have laid.
    """

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def __init__(self, path: str, title: str = None):
        """Constructor.

        TODO

        Args:
            path (str): The path to the graph's folder.
        """

        self.path: str = sanitize_path(path)
        """The path to the graph's folder.
        """

        # Generate hashed ID
        hash = hashlib.sha256(self.path.encode())
        self.id: str = hash.hexdigest() if path is not None else None
        """The hashed ID. The path is taken into account to generate it.
        """

        self.title = os.path.split(self.path)[-1] if title is None else title
        """The title of the graph. This is the name of the last folder in the
        graph's path.
        """

        # self.pages_file_name: list[str] = []
        # """List of pages file names belonging to this graph. Populated
        # by method get_pages().
        # """

        self.pages: list[Page] = []
        """List of parsed pages belonging to this graph. Populated by
        method parse().
        """


    # ----------------------------------
    #
    # Page factory.
    #
    # ----------------------------------
    def create_page(self, path: str=None, content: str=None, title: str=None):
        """Create a Page object.

        Args:
            path (str, optional): The path of the page. Defaults to None.
            content (str, optional): Content of the page. Defaults to None.
            title (str, optional): Title of the page. Defaults to None.

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_

        Yields:
            _type_: _description_
        """
        p = Page(path=path, content=content, title=title, graph=self)
        self.pages.append(p)

        return p


    # ----------------------------------
    #
    # Get all .md files in graph, but do not parse them.
    #
    # ----------------------------------
    def get_pages(self) -> None:
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
                    self.create_page(path=os.path.join(dirpath, fn))


    # ----------------------------------
    #
    # Read all pages in graph.
    #
    # ----------------------------------
    def parse(self) -> None:
        """Parses all pages in graph.
        """

        for p in self.pages:
            p.read_page_file()
            p.parse()
            yield p


    # ----------------------------------
    #
    # Get all blocks in graph.
    #
    # ----------------------------------
    def get_all_blocks(self) -> list[Any]:
        """Get all blocks in graph.

        Returns:
            list[Block]: A list of all blocks in graph.
        """
        blocks = []

        for page in self.pages:
            blocks.extend(page.blocks)

        return blocks
