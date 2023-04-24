from marko import Markdown
from marko.block import ListItem
from .block import Block
from typing import List
from .parser import Parser

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
        self.content: str = ""
        self.file_name: str = ""
        self.blocks: List[Block] = []


  def parse_markdown(self) -> any:
        """Parses the page's Markdown.

        Args:
            parser (Markdown): The parser.
            markdown (str): The Markdown string to parse.

        Returns:
            any: The parsed document.
        """
        blocks: list[str] = self.content.split("\n- ")

        # Process blocks
        for block in blocks:
            if not block.startswith("title::") or block.startswith("filters::"):
                block = block.strip('\n').strip(' ')
                self.blocks.append(Block(f"- {block}"))

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
            self.file_name = path
            return self
