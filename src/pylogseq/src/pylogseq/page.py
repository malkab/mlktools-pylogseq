from marko import Markdown
from marko.block import ListItem
from pylogseq.src.pylogseq.block import Block
from typing import List

# --------------------------------------
#
# Models a Logseq page.
#
# --------------------------------------
class Page():
  """Models a Logseq page."""

  # --------------------------------------
  #
  # Parses the page's Markdown.
  #
  # --------------------------------------
  def parseMarkdown(self, parser: Markdown, markdown: str) -> any:
    """Parses the page's Markdown.

    Args:
        parser (Markdown): The parser.
        markdown (str): The Markdown string to parse.

    Returns:
        any: The parsed document.
    """
    return parser.parse(markdown)

  # --------------------------------------
  #
  # Get and process blocks from a parsed Markdown.
  #
  # --------------------------------------
  def getBlocks(self, parsedMark: any) -> List[Block]:
    """Get and process blocks from a parsed Markdown.

    Args:
        parsedMark (any): The parsed Markdown objects.

    Returns:
        List[Block]: A list of parsed Block objects.
    """
    items: List[any] = [parsedMark]
    blocks: List[ListItem] = []
    out: List[Block] = []

    # Get ListItems (Blocks)
    while len(items)>0:

      i: any = items.pop(0)

      t: str = type(i).__name__

      if t == "ListItem":
        blocks.append(i)

      try:
        if t not in [ "RawText", "ListItem" ]:
          items.extend(i.children)
      except:
        pass

    print("D: jjjj", blocks)

    # Process Blocks
    for b in blocks:
      x = Block()
      x.process(b)
      out.append(x)

    return out
