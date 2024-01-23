import os
import re
from typing import Any, List

from pylogseq.block import Block

# TODO: DOCUMENT


# --------------------------------------
#
# Models a Logseq page.
#
# --------------------------------------
class Page:
    # --------------------------------------
    #
    # Constructor.
    #
    # --------------------------------------
    def __init__(
        self,
        path: str | None = None,
        content: str | None = None,
        title: str | None = None,
    ):
        """Contructor.

        Args:
            path (str, optional): Path, absolute or relative. Defaults to None.
            content (str, optional): Content. Defaults to None.
            title (str, optional): Title. Defaults to None.
        """

        self.path: str | None = (
            os.path.abspath(os.path.normpath(path)) if path is not None else None
        )
        """The path to the page's file.
        """

        self.content: str | None = content.strip("\n").strip() if content else None
        """The page's Markdown content.
        """

        self.title: str | None = (
            title
            if title
            else (os.path.split(self.path)[-1].strip(".md") if self.path else None)
        )
        """Page title: title if given in the constructor, the page file name
        if path is given, None otherwise. This member can be overrided if
        the page contains a title:: property block.
        """

    # ----------------------------------
    #
    # Parse the page's Markdown.
    #
    # ----------------------------------
    def parse(self) -> List[Block]:
        """Parses the page's Markdown.

        Args:
            parser (Markdown): The parser.
            markdown (str): The Markdown string to parse.

        Returns:
            any: The parsed document.
        """

        from pylogseq.pageparsererror import PageParserError

        blocks: List[str] = (
            self.content.split("\n- ") if self.content is not None else []
        )

        # Clean blocks
        for i, b in enumerate(blocks):
            blocks[i] = b.strip("\n").strip("-").strip()

        out: List[Block] = []

        # Check for the first block to be title:: or filter::
        if len(blocks) > 0:
            b0 = blocks[0]

            # Extract filter and title headers
            while blocks[0].startswith("title::") or blocks[0].startswith("filter::"):
                # Regex the title
                pattern = r"title::\s*(.+)\s*"
                match = re.search(pattern, b0)

                # Set the title if there is one in the reg exp
                if match is not None:
                    if match.group(1):
                        self.title = match.group(1).strip()

                # Drop the first block
                blocks.pop(0)

        # Process blocks
        for block in blocks:
            block_clean = block.strip("\n").strip()

            # Try to parse the block
            try:
                b = Block(content=f"- {block_clean}")
                b.parse()
                out.append(b)

            except Exception as e:
                raise PageParserError(
                    f"Error parsing block in page {self.path}: {e}",
                    e,
                    self,
                    block_clean,
                )

        return out

    # --------------------------------------
    #
    # Read the page file.
    #
    # --------------------------------------
    def read_page_file(self) -> Any:
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

        # Read the page file
        if self.path is not None:
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
        return f"Page(path={self.path}, title={self.title})"
