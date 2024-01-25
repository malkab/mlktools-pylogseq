import os
import fnmatch
from pylogseq.block import Block
from pylogseq.page import Page
from typing import Self, Generator

# TODO: DOCUMENT

"""Represents a Logseq Graph.
"""


class Graph:
    """Represents a Logseq Graph."""

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def __init__(self, path: str = ".", name: str | None = None):
        """The path can be relative or absolute, depending if it starts with "/" or not.

        Args:
            path (str, optional): Path to the graph's folder. Defaults to ".".
            name (str | None, optional): Given name of the graph. Defaults to None. If not given, it will be extracted from the path.
        """

        self.path: str = os.path.abspath(os.path.normpath(path))
        """The path to the graph's folder.
        """

        self._given_name = name
        """The name of the graph if it has been given. If not, it will try to
        get the name from the path."""

    # ----------------------
    #
    # Graph name taken from the path.
    #
    # ----------------------
    @property
    def name(self) -> str:
        """The graph's name.

        If a name was given in the constructor, it will be used. If not, it is extracted from the path.

        Returns:
            str: The name of the graph.
        """

        if self._given_name is not None:
            return self._given_name
        else:
            return self.path.split("/")[-1]

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

        pages: list[Page] = []

        for dirpath, dirnames, filenames in os.walk(self.path):
            page_file_n = fnmatch.filter(filenames, "*.md")

            for fn in page_file_n:
                # Filter all stuff at logseq/bak and at logseq/.recycle
                if "logseq/bak" not in dirpath and "logseq/.recycle" not in dirpath:
                    pages.append(Page(os.path.join(dirpath, fn)))

        return pages

    # ----------------------------------
    #
    # Read all pages in graph with an iterator.
    #
    # ----------------------------------
    def parse_iter(self) -> Generator[tuple[Self, Page, list[Block]], None, None]:
        """Parses all pages in the graph with an iterator. This must be used in
        a loop, very useful to check progress in the parsing process, for
        example:

        ```Python
        for p, b in graph.parse_iter():
            print(f"Page {p.title} parsed.")
            print(f"Number of blocks: {len(b)}"
        ```

        Yields:
            Page, list[Block]:
                Returns the Page that has been parsed and the list of Block
                that where processed.
        """
        for p in self.get_pages():
            p.read_page_file()
            blocks = p.parse()
            yield self, p, blocks

    # ----------------------------------
    #
    # __repr__
    #
    # ----------------------------------
    def __repr__(self) -> str:
        return f"Graph(name={self.name})"
