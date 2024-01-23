from pylogseq.graph import Graph, Block
from typing import List

from pylogseq.scrum_status import SCRUM_STATUS
# import pytest


# @pytest.mark.skip
class TestGraph:
    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    # @pytest.mark.skip
    def test_graph_constructor(self):
        # Bare constructor
        g = Graph()

        assert g.path is not None

        # Full, relative path
        g = Graph(path="tests/assets/pylogseq_test_graph")

        assert (
            g.path
            == "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph"
        )

        # Full, full path
        g = Graph(
            path="/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph"
        )

        assert (
            g.path
            == "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph"
        )

    # ----------------------------------
    #
    # Get pages from graph. Note that they aren't parsed yet.
    #
    # ----------------------------------
    # @pytest.mark.skip
    def test_get_pages(self):
        g = Graph("tests/assets/pylogseq_test_graph")

        pages = g.get_pages()

        assert sorted([p.path for p in pages if p.path is not None]) == [
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/journals/2023_03_30.md",
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/A.md",
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/SCRUM_TEST.md",
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md",
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_pages_folder/page.md",
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/almost_blank.md",
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/blank.md",
        ]

        assert [p.content for p in pages] == [None, None, None, None, None, None, None]

        assert sorted([p.title for p in pages if p.title is not None]) == [
            "2023_03_30",
            "A",
            "SCRUM_TEST",
            "a_page_with_a_title",
            "almost_blank",
            "blank",
            "page",
        ]

    # ----------------------
    #
    # SCRUM status
    #
    # ----------------------
    # @pytest.mark.skip
    def test_scrum_status(self):
        g = Graph("tests/assets/pylogseq_test_graph")

        pages = g.get_pages()

        for p in pages:
            p.read_page_file()

        blocks: List[Block] = []

        [blocks.extend(p.parse()) for p in pages]

        assert [b.scrum_status.name for b in blocks] == [
            "DOING",
            "DONE",
            "NONE",
            "NONE",
            "NONE",
            "ICEBOX",
            "BACKLOG",
            "BACKLOG",
            "CURRENT",
            "DOING",
            "DOING",
            "DONE",
            "WAITING",
            "NONE",
            "CURRENT",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "DONE",
            "NONE",
            "NONE",
            "DONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
        ]

        assert [b.scrum_time for b in blocks] == [
            8,
            0,
            0,
            0,
            0,
            0,
            1,
            5,
            3,
            8,
            23,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]

        assert [b.repetitive for b in blocks] == [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]

        assert [b.period for b in blocks] == [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "1 week",
            "2 semanas",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
