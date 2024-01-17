import os
import fnmatch
from pylogseq.block import Block
from pylogseq.page import Page
from typing import Generator, List, Tuple

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
    def __init__(self, path: str = "."):
        """Constructor.

        The path can be relative or absolute, depending if it starts with "/"
        or not.

        Args:
            path (str): The path to the graph's folder.
        """

        self.path: str = os.path.abspath(os.path.normpath(path))

        print()
        """The path to the graph's folder.
        """

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
    def parse_iter(self) -> Generator[Tuple[Page, List[Block]], None, None]:
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
            yield p, blocks

    # ----------------------------------
    #
    # __repr__
    #
    # ----------------------------------
    def __repr__(self) -> str:
        return f"Graph(path={self.path})"
