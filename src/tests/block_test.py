import sys
import os
sys.path \
  .insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pylogseq.src.pylogseq.block import Block

# --------------------------------------
#
# Common assets.
#
# --------------------------------------
blockExample = """





- DONE [#A] #A [[B]] Blocks title
  :LOGBOOK:
  CLOCK: [2023-01-11 Wed 12:39:45]--[2023-01-11 Wed 12:39:49] =>  00:00:04
  :END:
  pgh::whatver
  - Something




"""

blockExampleSanitized = """- DONE [#A] #A [[B]] Blocks title
  :LOGBOOK:
  CLOCK: [2023-01-11 Wed 12:39:45]--[2023-01-11 Wed 12:39:49] =>  00:00:04
  :END:
  pgh::whatver
  - Something"""

block = Block(blockExample)

# --------------------------------------
#
# Block tests.
#
# --------------------------------------
class TestBlock:

  # --------------------------------------
  #
  # Test constructor and initial members status
  #
  # --------------------------------------
  def test_constructor(self):
    # Check initial members status
    assert block.content == blockExampleSanitized
    assert block.content_hash == '655535623f9b06c58b7894d59a1540e2b4c7bfef92ba002f7ea5629da1162bb4'
    assert block.hash == None
    assert block.tags == []
    assert block.highest_priority == None
