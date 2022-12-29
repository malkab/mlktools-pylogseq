from marko import Markdown
from marko.block import ListItem
from pylogseq.src.pylogseq.block import Block
from typing import List
from pylogseq.src.pylogseq.mdlogseq.logseqparse import LogseqParse

class Parser:

  def __init__(self):
    pass

  def parse(self, markdown: str) -> None:
    parser = Markdown(extensions=[LogseqParse])
    return parser.parse(markdown)

  # def parse(self, markdown: str) -> None:
  #   """Parse the markdown string and return a list of blocks.

  #   Args:
  #       markdown (str): The markdown string to parse.

  #   Returns:
  #       list: A list of blocks.
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
