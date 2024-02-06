from pylogseq.pylogseq.graph import Block, Graph

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
        assert g.name == "src"

        # Full, relative path
        g = Graph(path="tests/assets/pylogseq_test_graph")

        assert (
            g.path
            == "/home/git/mlktools/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph"
        )
        assert g.name == "pylogseq_test_graph"

        # Full, full path
        g = Graph(
            path="/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph",
            name="grafo",
        )

        assert (
            g.path
            == "/home/git/mlktools/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph"
        )
        assert g.name == "grafo"

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
            "/home/git/mlktools/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/journals/2023_03_30.md",
            "/home/git/mlktools/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/A.md",
            "/home/git/mlktools/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/SCRUM_TEST.md",
            "/home/git/mlktools/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md",
            "/home/git/mlktools/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/a_pages_folder/page.md",
            "/home/git/mlktools/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/almost_blank.md",
            "/home/git/mlktools/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/blank.md",
            "/home/git/mlktools/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/page_with_properties.md",
        ]

        assert [p.content for p in pages] == [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        assert sorted([p.title for p in pages if p.title is not None]) == [
            "2023_03_30",
            "A",
            "SCRUM_TEST",
            "a_page_with_a_title",
            "almost_blank",
            "blank",
            "page",
            "page_with_properties",
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

        blocks: list[Block] = []

        [blocks.extend(p.parse()) for p in pages]

        assert sorted([b.scrum_status.name for b in blocks]) == [
            "BACKLOG",
            "BACKLOG",
            "CURRENT",
            "CURRENT",
            "CURRENT",
            "DOING",
            "DOING",
            "DOING",
            "DOING",
            "DONE",
            "DONE",
            "DONE",
            "DONE",
            "ICEBOX",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "NONE",
            "WAITING",
        ]

        assert sorted([b.scrum_time for b in blocks]) == [
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
            1,
            1,
            1,
            1,
            1,
            3,
            5,
            8,
            8,
            23,
        ]

        assert sorted([b.repetitive for b in blocks]) == [
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
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
        ]

        assert sorted([b.repetitive_priority for b in blocks]) == [
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
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
        ]

        assert sorted([str(b.repetitive_period) for b in blocks]) == [
            "1",
            "2",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
        ]

        assert sorted([str(b.repetitive_score is not None) for b in blocks]) == [
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "False",
            "True",
            "True",
        ]
