import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from marko import Markdown
from pylogseq.src.pylogseq.mdlogseq.logseqparse import LogseqParse
from pylogseq.src.pylogseq.block import Block

g = LogseqParse()
mark = Markdown(extensions=[LogseqParse])

markdown = """
- DONE #[[A/B/C/Gestión general]] Something
  :LOGBOOK:
  CLOCK: [2022-11-25 Fri 08:57:12]--[2022-11-25 Fri 09:09:45] =>  00:12:33
  CLOCK: [2022-11-25 Fri 10:01:13]--[2022-11-25 Fri 10:01:17] =>  00:00:04
  CLOCK: [2022-11-25 Fri 10:01:18]--[2022-11-25 Fri 10:07:58] =>  00:06:40
  CLOCK: [2022-11-25 Fri 12:17:38]--[2022-11-25 Fri 12:19:27] =>  00:01:49
  CLOCK: [2022-11-25 Fri 14:49:56]--[2022-11-25 Fri 14:54:06] =>  00:04:10
  :END:
  - A
  - B
  """

parsed = mark.parse(markdown)

items = [parsed]

loop = True

txt = ""

blocks = []

while loop:

  loop = False

  for i in items:
    t = type(i).__name__

    print("\nTYPE: ", t)

    if t in [ "Document", "List", "Paragraph"]:
      loop = True
      items = i.children

    if t == "ListItem" :
      blocks.append(i)
      loop = True
      items = i.children

    if t == "RawText":
      print(i)

print(blocks)

print(blocks[0])

print()
