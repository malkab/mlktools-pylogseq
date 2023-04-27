from pylogseq.page import Page
from pylogseq.graph import Graph
from pylogseq.parser import Parser

import pytest


# @pytest.mark.skip
class TestPage:

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def test_page_constructor(self):
        """Test the page's constructor.
        """

        # Bare constructor
        p = Page()

        assert p.path is None
        assert p.id is None
        assert p.content is None
        assert p.title is None
        assert p.graph is None
        assert p.blocks == []

        # Optional path
        p = Page(path="tests/assets/pylogseq_test_graph/pages/test_page.md")

        assert p.path == "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/test_page.md"
        assert p.id == "135c3d93c73dc9c32abc752c1509bdb01d3025027027ef9fe6c3699a08a91091"
        assert p.content is None
        assert p.title == "test_page"
        assert p.graph is None
        assert p.blocks == []

        # Optional content
        p = Page(content="- Block")

        assert p.path is None
        assert p.id is None
        assert p.content == "- Block"
        assert p.title is None
        assert p.graph is None
        assert p.blocks == []

        # Optional title
        p = Page(title="Page title")

        assert p.path is None
        assert p.content is None
        assert p.title == "Page title"
        assert p.graph is None
        assert p.blocks == []

        # Optional graph
        g = Graph("tests/assets/pylogseq_test_graph")
        p = Page(graph=g)

        assert p.path is None
        assert p.content is None
        assert p.title is None
        assert isinstance(p.graph, Graph)
        assert p.graph.title == "pylogseq_test_graph"
        assert p.blocks == []

        # Full
        g = Graph("tests/assets/pylogseq_test_graph")
        p = Page(path="tests/assets/pylogseq_test_graph/pages/test_page.md",
                 content="- Block",
                 title="Page title",
                 graph=g)

        assert p.path == "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/test_page.md"
        assert p.id == "135c3d93c73dc9c32abc752c1509bdb01d3025027027ef9fe6c3699a08a91091"
        assert p.content == "- Block"
        assert p.title == "Page title"
        assert isinstance(p.graph, Graph)
        assert p.graph.title == "pylogseq_test_graph"
        assert p.blocks == []

    # ----------------------------------
    #
    # Block comment
    #
    # ----------------------------------
    def test_parse(self):
        # A Page object
        p = Page(path="tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md")

        # Read a page
        p.read_page_file()

        assert p.path == "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md"
        assert p.id == "d2a8918f9d2f71a17e0762549f0d4f4dbf2aaeb6cf8bd7eaeb8ec00108406931"
        assert p.content == 'title:: A new title for the test_page set with a "title" property\n\n- Do not remove this test page, it is used in [[Python]] tests.\n- This is a block.'
        assert p.title == "a_page_with_a_title"
        assert p.graph == None
        assert p.blocks == []

        # Check the blocks
        p.parse()

        assert p.path == "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md"
        assert p.id == "d2a8918f9d2f71a17e0762549f0d4f4dbf2aaeb6cf8bd7eaeb8ec00108406931"
        assert p.content == 'title:: A new title for the test_page set with a "title" property\n\n- Do not remove this test page, it is used in [[Python]] tests.\n- This is a block.'
        assert p.title == 'A new title for the test_page set with a "title" property'
        assert p.graph == None

        block_titles = [ (b.order_in_page, b.title,) for b in p.blocks ]

        assert block_titles == [
            (0, "Do not remove this test page, it is used in [[Python]] tests.",),
            (1, 'This is a block.',)
        ]
