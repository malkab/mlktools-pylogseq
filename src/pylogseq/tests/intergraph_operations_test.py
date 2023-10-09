import pytest
from typing import List

from pylogseq.page import Page
from pylogseq.block import Block

# ----------------------------------
#
# Tests operations between two graphs.
#
# ----------------------------------

#@pytest.mark.skip
class TestIntergraphOperations:
    # TODO: AUTODOCSTRING HERE (C+S+2)

    # ----------------------------------
    #
    # Test opening comment
    #
    # ----------------------------------
    #@pytest.mark.skip
    def test_test_name(self):
        # TODO: AUTODOCSTRING HERE (C+S+2)

        # Read a page in graph_a
        page_a = Page(path="tests/assets/graph_a/journals/2023_03_30.md")

        blocks: List[Block] = page_a.read_page_file()

        # Parse it
        page_a.parse()

        TODO: MOVE A BLOCK BETWEEN GRAPHS
