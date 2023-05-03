import os
import fnmatch
import hashlib
from .page import Page
from .block import Block
from typing import Any
from .common import sanitize_path
from .forward_declarations import Graph

"""Represents a Logseq Graph.
"""

class Graph():
    """Represents a Logseq Graph.

    PATH puede ir en relativo o absoluto, dependiendo si comienza por / o no.

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
    def __init__(self, path: str=None, title: str=None):
        """Constructor.

        TODO

        Args:
            path (str): The path to the graph's folder.
        """

        self.path: str = os.path.abspath(sanitize_path(path)) if path else None
        """The path to the graph's folder.
        """

        # Set title
        self.title = None
        """The title of the graph. This is the name of the last folder in the
        graph's path.
        """

        if title:
            self.title = title
        elif self.path:
            self.title = os.path.split(self.path)[-1]

        self.pages: list[Page] = []
        """List of parsed pages belonging to this graph. Populated by
        method parse().
        """


    # ----------------------------------
    #
    # Property id.
    # ID of the grap.
    #
    # ----------------------------------
    @property
    def id(self) -> str:
        """The hashed ID. It depends on the path. Child pages and blocks will
        depend on this too.
        """
        if self.path is None:
            raise Exception("Can't compute ID for Graph since path is None")

        hash = hashlib.sha256(self.path.encode())
        return hash.hexdigest()


    # ----------------------------------
    #
    # Page factory.
    #
    # ----------------------------------
    def create_page(self, path: str=None, content: str=None, title: str=None) -> Page:
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
        page = Page(path=path, content=content, title=title, graph=self)
        self.pages.append(page)

        return page


    # ----------------------------------
    #
    # Add page.
    #
    # ----------------------------------
    def add_page(self, page: Page) -> Graph:
        """Add a Page object to the graph.

        Args:
            page (Page): The page to add.
        """
        page.graph = self
        self.pages.append(page)

        return self


    # ----------------------------------
    #
    # Get all .md files in graph, but do not parse them.
    #
    # ----------------------------------
    def get_pages(self) -> list[Page]:
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

                    # Substract from the page path the path of the graph so the
                    # page's path is relative to the graph
                    gp = self.path.split("/")
                    pp = os.path.join(dirpath, fn).split("/")
                    common_prefix = 0

                    min_len = min(len(gp), len(pp))

                    for i in range(min_len):
                        if gp[i] == pp[i]:
                            common_prefix += 1
                        else:
                            break

                    fp = "/".join(pp[common_prefix:])

                    self.create_page(path=fp)

        return self.pages

    # ----------------------------------
    #
    # Read all pages in graph in bulk.
    #
    # ----------------------------------
    def parse(self) -> Graph:
        """Parses all pages in graph in bulk.
        """
        for p in self.pages:
            p.read_page_file()
            p.parse()

        return self


    # ----------------------------------
    #
    # Read all pages in graph with an iterator.
    #
    # ----------------------------------
    def parse_iter(self) -> None:
        """Parses all pages in graph with an iterator. This must be used in a
        loop, very useful to check progress in the parsing process and such:

        ```Python
        for p in graph.parse_iter():
            print(f"Page {p.title} parsed.")
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
    def get_all_blocks(self) -> list[Block]:
        """Get all blocks in graph.

        Returns:
            list[Block]: A list of all blocks in graph.
        """
        blocks: list[Block] = []

        for page in self.pages:
            blocks.extend(page.blocks)

        return blocks


    # ----------------------------------
    #
    # __repr__
    #
    # ----------------------------------
    def __repr__(self) -> str:
        return f"Graph(path={self.path}, title={self.title})"
