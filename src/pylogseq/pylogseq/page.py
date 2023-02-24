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
    self.blocks: List[Block] = []


  def parseMarkdown(self) -> any:
    """Parses the page's Markdown.

    Args:
        parser (Markdown): The parser.
        markdown (str): The Markdown string to parse.

    Returns:
        any: The parsed document.
    """
    blocks: list[str] = self.content.split("\n- ")

    b = []
    for block in blocks:
      if not block.startswith("title::") or block.startswith("filters::"):
        block = block.strip('\n').strip(' ')
        b.append(f"- {block}")

    for block in b:
      # print("D: 000", block)

      b = Block(block)

      print("D: 888", b.now, b.done, b.later)


    # parser = Markdown(extensions=[Parser])

    # return parser.parse(self.content)



  # # --------------------------------------
  # #
  # # Get and process blocks from a parsed Markdown.
  # #
  # # --------------------------------------
  # def getBlocks(self, parsedMark: any) -> any:
  #   """Get and process blocks from a parsed Markdown.

  #   Args:
  #       parsedMark (any): The parsed Markdown objects.

  #   Returns:
  #       List[Block]: A list of parsed Block objects.
  #   """
  #   items: List[any] = [parsedMark]
  #   blocks: List[ListItem] = []
  #   out: List[Block] = []

  #   # Get ListItems (Blocks)
  #   while len(items)>0:

  #     i: any = items.pop(0)

  #     t: str = type(i).__name__

  #     if t == "ListItem":
  #       blocks.append(i)

  #     try:
  #       if t not in [ "RawText", "ListItem" ]:
  #         items.extend(i.children)
  #     except:
  #       pass

  #   # Process Blocks
  #   for b in blocks:
  #     x = Block()
  #     x.process(b)
  #     self.blocks.append(x)

  #   return self

  # --------------------------------------
  #
  # Read the page file.
  #
  # --------------------------------------
  def readPageFile(self, path: str) -> any:
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
      return self
