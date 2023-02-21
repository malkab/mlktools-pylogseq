from marko import Markdown
from marko.block import ListItem
from pylogseq.src.pylogseq.block import Block
from typing import List
from mdlogseq.logseqparse import LogseqParse

class Parser:

  def __init__(self):
    pass

  def parse(self, markdown: str) -> None:
    parser = Markdown(extensions=[LogseqParse])

    return parser.parse(markdown)
