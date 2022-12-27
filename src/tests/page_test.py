import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

# --------------------------------------
#
# Page tests.
#
# --------------------------------------
class TestPage:

  # --------------------------------------
  #
  # Loads a page from file.
  #
  # --------------------------------------
  def test_a(self):

    assert True == True;

    assert 3 > 2;

    assert 2 > 3;
