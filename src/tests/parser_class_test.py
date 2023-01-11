import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pylogseq.src.pylogseq.parser import Parser

@pytest.mark.skip
class TestParserClass:
  def test_parse(self):
    parser = Parser()
