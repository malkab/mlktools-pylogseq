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

        with pytest.raises(Exception, match="Can't compute abs_path for Page since graph is None"):
            p.abs_path

        with pytest.raises(Exception, match="Can't compute ID for Page since path is None"):
            p.id

        assert p.content is None
        assert p.title is None
        assert p.graph is None
        assert p.blocks == []

        # Optional path
        p = Page(path="pages/test_page.md")

        assert p.path == "pages/test_page.md"

        with pytest.raises(Exception, match="Can't compute abs_path for Page since graph is None"):
            p.abs_path

        with pytest.raises(Exception, match="Can't compute ID for Page: check parent graph exists and that has a valid ID"):
            p.id

        assert p.content is None
        assert p.title == "test_page"
        assert p.graph is None
        assert p.blocks == []

        # Optional content
        p = Page(content="- Block")

        assert p.path is None

        with pytest.raises(Exception, match="Can't compute abs_path for Page since graph is None"):
            p.abs_path

        with pytest.raises(Exception, match="Can't compute ID for Page since path is None"):
            p.id

        assert p.content == "- Block"
        assert p.title is None
        assert p.graph is None
        assert p.blocks == []

        # Optional title
        p = Page(title="Page title")

        assert p.path is None

        with pytest.raises(Exception, match="Can't compute abs_path for Page since graph is None"):
            p.abs_path

        with pytest.raises(Exception, match="Can't compute ID for Page since path is None"):
            p.id

        assert p.content is None
        assert p.title == "Page title"
        assert p.graph is None
        assert p.blocks == []

        # Optional graph
        g = Graph("tests/assets/pylogseq_test_graph")
        p = Page(graph=g)

        assert p.path is None

        with pytest.raises(Exception, match="Can't compute abs_path for Page since path is None"):
            p.abs_path

        with pytest.raises(Exception, match="Can't compute ID for Page since path is None"):
            p.id

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

        assert p.path == "tests/assets/pylogseq_test_graph/pages/test_page.md"
        assert p.abs_path == \
            "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/tests/assets/pylogseq_test_graph/pages/test_page.md"
        assert p.id == \
            "4c656219ac9b302421ebf5315384ded4497ae624c809ec9e41039bdec7a25448"
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
        g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

        # A Page object
        p = g.create_page(path="pages/a_page_with_a_title.md")

        # Read a page
        p.read_page_file()

        assert p.path == "pages/a_page_with_a_title.md"
        assert p.abs_path == \
            "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md"
        assert p.id == \
            "4c3c23df51866eef3feea319a845c217f94070007a5001cae0de7a0aed85b6b7"
        assert p.content == \
            'title:: A new title for the test_page set with a "title" property\nfilter:: a filter\n\n- Do not remove this test page, it is used in [[Python]] tests.\n- This is a block.'
        assert p.title == "a_page_with_a_title"
        assert p.graph == g
        assert p.blocks == []

        # Check the blocks
        p.parse()

        assert p.path == "pages/a_page_with_a_title.md"
        assert p.abs_path == \
            "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md"
        assert p.id == \
            "4c3c23df51866eef3feea319a845c217f94070007a5001cae0de7a0aed85b6b7"
        assert p.content == \
            'title:: A new title for the test_page set with a "title" property\nfilter:: a filter\n\n- Do not remove this test page, it is used in [[Python]] tests.\n- This is a block.'
        assert p.title == 'A new title for the test_page set with a "title" property'
        assert p.graph == g

        block_titles = [ (b.order_in_page, b.title,) for b in p.blocks ]

        assert block_titles == [
            (0, "Do not remove this test page, it is used in [[Python]] tests.",),
            (1, 'This is a block.',)
        ]
