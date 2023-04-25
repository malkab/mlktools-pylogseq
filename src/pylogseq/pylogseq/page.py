from .block import Block
from typing import List
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
  def __init__(self):
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
        from .graph import Graph

        self.content: str = None
        self.path: str = None
        self.blocks: List[Block] = []
        self.graph: Graph = None
        self.title: str = None


  def parse(self) -> any:
        """Parses the page's Markdown.

        Args:
            parser (Markdown): The parser.
            markdown (str): The Markdown string to parse.

        Returns:
            any: The parsed document.
        """
        from .pageparsererror import PageParserError

        blocks: list[str] = self.content.split("\n- ")

        # Process blocks
        for block in blocks:
            if not block.startswith("title::") or block.startswith("filters::"):
                block_clean = block.strip('\n').strip(' ')

                # Try to parse the block
                try:
                    b = Block(f"- {block_clean}")
                except Exception as e:
                    raise PageParserError(
                        f"Error parsing block in page {self.path}: {e}",
                        e, self, block_clean)

                b.page = self

                self.blocks.append(b)

  # --------------------------------------
  #
  # Read the page file.
  #
  # --------------------------------------
  def read_page_file(self, path: str) -> any:
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
        with open(path, "r") as f:
            self.content = f.read()
            self.path = path
            self.title = os.path.split(self.path)[-1]

            return self
