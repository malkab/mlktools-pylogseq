import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from marko import Markdown
import marko
from pylogseq.src.pylogseq.mdlogseq.logseqparse import LogseqParse

# --------------------------------------
#
# Markdown parsing tests.
#
# --------------------------------------
class TestMarkdownParser:

  # --------------------------------------
  #
  # Parses
  # CLOCK: [2022-11-25 Fri 12:17:38]--[2022-11-25 Fri 12:19:27] =>  00:01:49
  # items
  #
  # --------------------------------------
  def test_clock(self):

    g = LogseqParse()
    mark = Markdown(extensions=[LogseqParse])

    markdown = """- DONE #[[Gestión general]]
  :LOGBOOK:
  CLOCK: [2022-11-25 Fri 08:57:12]--[2022-11-25 Fri 09:09:45] =>  00:12:33
  CLOCK: [2022-11-25 Fri 10:01:13]--[2022-11-25 Fri 10:01:17] =>  00:00:04
  CLOCK: [2022-11-25 Fri 10:01:18]--[2022-11-25 Fri 10:07:58] =>  00:06:40
  CLOCK: [2022-11-25 Fri 12:17:38]--[2022-11-25 Fri 12:19:27] =>  00:01:49
  CLOCK: [2022-11-25 Fri 14:49:56]--[2022-11-25 Fri 14:54:06] =>  00:04:10
  :END:"""

    parsed = mark.parse(markdown)

    print("D: ", parsed.children[0])

    assert isinstance(parsed, marko.block.Document) == True
    # assert isinstance(parsed.children, marko.block.List) == True
