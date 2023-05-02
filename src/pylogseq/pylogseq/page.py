import hashlib
from .forward_declarations import Graph
from .common import sanitize_path, sanitize_content
from enum import Enum
import os
import re


# --------------------------------------
#
# Models a Logseq page.
#
# --------------------------------------
class Page():
    """
    Docstring

    Attributes
    ----------
    exposure : float
        Exposure in seconds.

    Methods
    -------
    colorspace(c='rgb')
        Represent the photo in the given colorspace.
    gamma(n=1.0)
        Change the photo's gamma exposure.
    """

    # --------------------------------------
    #
    # Constructor.
    #
    # --------------------------------------
    def __init__(self, path: str=None, content: str=None, title: str=None,
                 graph: Graph=None):
            """
            Docstring

            Parameters
            ----------
            var : type
                Doc

            Returns
            -------
            type
                Doc
            """
            from .block import Block
            from .graph import Graph

            self.path: str = sanitize_path(path)
            """The path to the page's file.
            """

            self.content: str = sanitize_content(content) if content else None
            """The page's Markdown content.
            """

            self.title: str = \
                title if title else (os.path.split(self.path)[-1].strip(".md") if self.path else None)
            """Page title: title if given in the constructor, the page file name
            if path is given, None otherwise. This member can be overrided if
            the page contains a title:: property block.
            """

            self.graph: Graph = graph
            """The graph this page belongs to.
            """

            self.blocks: list[Block] = []
            """List of parsed blocks belonging to this page. Populated by the
            parse() method.
            """


    # ----------------------------------
    #
    # Property id.
    # ID of the grap.
    #
    # ----------------------------------
    @property
    def id(self) -> str:
        """The hashed ID. It depends on the path and the ID of the parent graph.
        Child blocks will depend on this too.
        """
        if self.path is None:
            raise Exception("Page has no path and/or page's graph has no ID, cannot generate ID.")

        try:
            hash = f"{self.graph.id}{self.path}"
            hash = hashlib.sha256(hash.encode())
            return hash.hexdigest()
        except:
            raise Exception("Page has no path and/or page's graph has no ID, cannot generate ID.")


    # ----------------------------------
    #
    # Property abs_path.
    # Absolute path of the page, including the path of the graph.
    #
    # ----------------------------------
    @property
    def abs_path(self) -> str:
        try:
            return os.path.join(self.graph.path, self.path)
        except:
             raise Exception("Page has no path and/or page's graph has no path, cannot generate absolute path.")


    # ----------------------------------
    #
    # Parse the page's Markdown.
    #
    # ----------------------------------
    def parse(self) -> any:
            """Parses the page's Markdown.

            Args:
                parser (Markdown): The parser.
                markdown (str): The Markdown string to parse.

            Returns:
                any: The parsed document.
            """
            from .pageparsererror import PageParserError
            from .block import Block

            blocks: list[str] = self.content.split("\n- ")

            # Check for the first block to be title:: or filter::
            b0 = blocks[0]

            if b0.startswith("title::") or b0.startswith("filter::"):
                # Extract the block so it's not processed as a block
                b0 = blocks.pop(0)

                # Regex the title
                pattern = r'title::\s*(.+)\s*'
                match = re.search(pattern, b0)

                # Set the title if there is one in the reg exp
                if match.group(1):
                    self.title = match.group(1).strip()

            # Process blocks
            for block in blocks:
                block_clean = block.strip('\n').strip()

                # Try to parse the block
                try:
                    b = Block(content=f"- {block_clean}", page=self)
                except Exception as e:
                    raise PageParserError(
                        f"Error parsing block in page {self.path}: {e}",
                        e, self, block_clean)

                # Add the block to the page
                b.page = self
                b.order_in_page = len(self.blocks)
                self.blocks.append(b)

    # --------------------------------------
    #
    # Read the page file.
    #
    # --------------------------------------
    def read_page_file(self) -> any:
            """
            Docstring

            Parameters
            ----------
            var : type
                Doc

            Returns
            -------
            type
                Page
            """
            # Raise exception if path is None
            if self.path is None:
                raise Exception("Page path is None.")

            # Read the page file
            with open(self.path, "r") as f:
                self.content = sanitize_content(f.read())

                return self


    def __repr__(self) -> str:
        return(f"Page(path={self.path}, title={self.title}, )")
