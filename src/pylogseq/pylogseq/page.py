import os
from typing import Any
from urllib.parse import unquote

from .block import Block
from .parser import Parser

from .mdlogseq.elements_parsers.logseqtagclass import LogseqTag

from marko import block as m_block
from marko import inline as m_inline

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
            else (
                unquote(os.path.splitext(os.path.basename(str(self.path)))[0])
                if self.path
                else None
            )
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
    def parse(self, debug: bool = False):  # -> List[Block]:
        """Parses the page's Markdown.

        Args:
            parser (Markdown): The parser.
            markdown (str): The Markdown string to parse.

        Returns:
            any: The parsed document.
        """

        # from pylogseq.pageparsererror import PageParserError

        # blocks: List[str] = (
        #     self.content.split("\n- ") if self.content is not None else []
        # )

        # # Clean blocks
        # for i, b in enumerate(blocks):
        #     blocks[i] = b.strip("\n").strip("-").strip()

        # # Check for the first block to be title:: or filter::
        # if len(blocks) > 0:
        #     b0 = blocks[0]

        #     # Extract filter and title headers
        #     while b0.startswith("title::") or b0.startswith("filter::"):
        #         # Regex the title
        #         pattern = r"title::\s*(.+)\s*"
        #         match = re.search(pattern, b0)

        #         # Set the title if there is one in the reg exp
        #         if match is not None:
        #             if match.group(1):
        #                 self.title = match.group(1).strip()

        #         # Drop the first block
        #         blocks.pop(0)

        # # Process blocks
        # for block in blocks:
        #     block_clean = block.strip("\n").strip()

        #     # Try to parse the block
        #     try:
        #         b = Block(content=f"- {block_clean}")
        #         b.parse()
        #         out.append(b)

        #     except Exception as e:
        #         raise PageParserError(
        #             f"Error parsing block in page {self.path}: {e}",
        #             e,
        #             self,
        #             block_clean,
        #         )

        object_list = []

        parser: Parser = Parser()

        if self.content is not None:
            object = parser.parse(self.content)

            # Parse out
            self.parse_recursive(object, object_list, debug=debug)

        return object_list

    # ----------------------
    #
    # Recursive parsing.
    #
    # ----------------------
    def parse_recursive(self, object, object_list: list, debug: bool = False):
        """Recursive parsing.

        Args:
            block (Block): The block to parse.

        Returns:
            Block: The parsed block.
        """

        # ----
        # marko.Block.Document
        # ----
        if isinstance(object, m_block.Document):
            if debug:
                print(
                    f"Found marko.Block.Document with {len(object.children)} children, processing children"
                )

            # Process children
            if len(object.children) > 0:
                for child in object.children:
                    self.parse_recursive(child, object_list, debug=debug)

        # ----
        # marko.Block.paragraph
        # ----
        elif isinstance(object, m_block.Paragraph):
            block = self.check_for_block(object_list)

            if block is not None:
                if debug:
                    print(
                        f"Found marko.Block.Paragraph with preceding Block with {len(object.children)} children, adding content to the preceding Block"
                    )

                # There is a parent Block, process children, if any
                if len(object.children) > 0:
                    for child in object.children:
                        self.parse_recursive(child, object_list, debug=debug)

            SEGUIR AQUÍ

            else:
                if debug:
                    print(
                        "Found marko.Block.Paragraph without preceding Block, ignoring"
                    )

        # ----
        # marko.Block.RawText
        # ----
        elif isinstance(object, m_inline.RawText):
            if debug:
                print(f"Found marko.Inline.RawText, text '{object.children}'")

        # ----
        # marko.Block.List
        # ----
        elif isinstance(object, m_block.List):
            if debug:
                print(
                    f"Found marko.Block.List with {len(object.children)} children, processing children"
                )

            # Process children
            if len(object.children) > 0:
                for child in object.children:
                    self.parse_recursive(child, object_list, debug=debug)

        # ----
        # marko.Block.ListItem
        # ----
        elif isinstance(object, m_block.ListItem):
            if debug:
                print(
                    f"Found marko.Block.ListItem with {len(object.children)} children, adding a new Block and processing children"
                )

            # As ListItem, add a Block to the list to start processing children that affects it
            object_list.append(Block(content=""))

            # Process children
            if len(object.children) > 0:
                for child in object.children:
                    print("D: ", child)

                    self.parse_recursive(child, object_list, debug=debug)

        # ----
        # pylogseq.mdlogseq.elements_parsers.logseqtagclass.LogseqTag
        # ----
        elif isinstance(object, LogseqTag):
            print("D: KKKKKKK")

        # ----
        # marko.inline.LineBreak
        # ----
        elif isinstance(object, m_inline.LineBreak):
            if debug:
                print("Found marko.Inline.LineBreak")

        # ----
        # Unknown object type
        # ----
        else:
            raise Exception(f"Unknown object type {type(object)}")

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

    # --------------------------------------
    #
    # Check if the last item in recurring parser object_list is a Block.
    # If it is, return it, if not, return None.
    #
    # --------------------------------------
    def check_for_block(self, object_list: list) -> Block | None:
        if len(object_list) > 0:
            if isinstance(object_list[-1], Block):
                return object_list[-1]

        return None

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
        return f"Page(title={self.title})"
