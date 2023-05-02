import hashlib
from .forward_declarations import Graph
from .common import sanitize_path, sanitize_content
import os

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
    def __init__(self, path: str = None, content: str = None, title: str = None,
                 graph: Graph = None):
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

            self.title = \
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

            hash = hashlib.sha256(self.path.encode()) if path else None
            self.id: str = hash.hexdigest() if hash else None
            """Generated hashed ID. Based on the path."""


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

            # Process blocks
            for block in blocks:
                if not block.startswith("filters::"):
                    block_clean = block.strip('\n').strip()

                    # Try to parse the block
                    try:
                        b = Block(content=f"- {block_clean}", page=self)
                    except Exception as e:
                        raise PageParserError(
                            f"Error parsing block in page {self.path}: {e}",
                            e, self, block_clean)

                    # Add the block to the page if not a title
                    if not b.is_title_block:
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
