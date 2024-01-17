from pylogseq.graph import Graph
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
        g = Graph(path="tests/assets/pylogseq_test_graph/pages/test_page.md")

        assert (
            g.path
            == "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/test_page.md"
        )

        # Full, full path
        g = Graph(
            path="/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/test_page.md"
        )

        assert (
            g.path
            == "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/test_page.md"
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

        assert sorted([p.path for p in pages]) == [
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/journals/2023_03_30.md",
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/A.md",
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/SCRUM_TEST.md",
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md",
            "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_pages_folder/page.md",
        ]

        assert [p.content for p in pages] == [None, None, None, None, None]

        assert sorted([p.title for p in pages]) == [
            "2023_03_30",
            "A",
            "SCRUM_TEST",
            "a_page_with_a_title",
            "page",
        ]
