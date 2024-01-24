from pylogseq.page import Page
from pylogseq.block import Block
import pytest

import os


# @pytest.mark.skip
class TestPage:
    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def test_page_constructor(self):
        """Test the page's constructor."""

        # Bare constructor
        p = Page()

        assert p.path is None
        assert p.content is None
        assert p.title is None

        # Optional path
        p = Page(path="tests/assets/pylogseq_test_graph/pages/test_page.md")

        assert (
            p.path
            == "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/test_page.md"
        )

        assert p.content is None
        assert p.title == "test_page"

        # Optional content
        p = Page(path="", content="- Block")

        assert p.path == "/home/git/mlktools/mlktools-pylogseq/src/pylogseq"

        assert p.content == "- Block"
        assert p.title == "pylogseq"

        # Optional title
        p = Page(title="Page title")

        assert p.path is None

        assert p.content is None
        assert p.title == "Page title"

        # Full
        p = Page(
            path="tests/assets/pylogseq_test_graph/pages/test_page.md",
            content="- Block",
            title="Page title",
        )

        assert (
            p.path
            == "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/test_page.md"
        )
        assert p.content == "- Block"
        assert p.title == "Page title"

    # ----------------------------------
    #
    # Block comment
    #
    # ----------------------------------
    def test_parse(self):
        # A Page object
        p = Page(
            path="/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md"
        )

        assert (
            p.path
            == "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md"
        )

        # Read a page
        p.read_page_file()

        assert (
            p.content
            == 'title:: A new title for the test_page set with a "title" property\nfilter:: a filter\n\n- Do not remove this test page, it is used in [[Python]] tests.\n- This is a block.'
        )

        assert p.title == "a_page_with_a_title"

        # Check the blocks
        blocks: list[Block] = p.parse()

        assert (
            p.content
            == 'title:: A new title for the test_page set with a "title" property\nfilter:: a filter\n\n- Do not remove this test page, it is used in [[Python]] tests.\n- This is a block.'
        )

        assert p.title == "a_page_with_a_title"

        block_titles = [b.title for b in blocks]

        assert block_titles == [
            'title:: A new title for the test_page set with a "title" property',
            "Do not remove this test page, it is used in [[Python]] tests.",
            "This is a block.",
        ]
