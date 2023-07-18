from pylogseq.block import Block
from pylogseq.pageparsererror import PageParserError
import os
import re

# TODO: DOCUMENT


# --------------------------------------
#
# Models a Logseq page.
#
# --------------------------------------
class Page():

    # --------------------------------------
    #
    # Constructor.
    #
    # --------------------------------------
    def __init__(self, path: str=None, content: str=None, title: str=None):
        """Contructor.

        Args:
            path (str, optional): Path, absolute or relative. Defaults to None.
            content (str, optional): Content. Defaults to None.
            title (str, optional): Title. Defaults to None.
        """


        self.path: str = os.path.abspath(
            os.path.normpath(path)) if path else None
        """The path to the page's file.
        """

        self.content: str = content.strip("\n").strip() if content else None
        """The page's Markdown content.
        """

        self.title: str = \
            title if title else (os.path.split(self.path)[-1].strip(".md") if self.path else None)
        """Page title: title if given in the constructor, the page file name
        if path is given, None otherwise. This member can be overrided if
        the page contains a title:: property block.
        """


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

        blocks: list[str] = self.content.split("\n- ")

        out: list[Block] = []

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
                b = Block(content=f"- {block_clean}")
                b.parse()
                out.append(b)

            except Exception as e:
                raise PageParserError(
                    f"Error parsing block in page {self.path}: {e}",
                    e, self, block_clean)

        return out


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

        # Read the page file
        with open(self.path, "r") as f:
            self.content = (f.read()).strip("\n").strip()

            return self


    # ----------------------------------
    #
    # __repr__
    #
    # ----------------------------------
    def __repr__(self) -> str:
        """Representación __repr__.

        Returns:
            str: La representación del objeto para los print.
        """
        return(f"Page(path={self.path}, title={self.title})")
