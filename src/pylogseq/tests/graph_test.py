from pylogseq.graph import Graph
from pylogseq.page import Page
import pytest

#@pytest.mark.skip
class TestGraph:

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    #@pytest.mark.skip
    def test_graph_constructor(self):

        # Bare constructor
        g = Graph()

        assert g.path is None

        # Optional path
        g = Graph(path="tests/assets/pylogseq_test_graph")

        assert g.path == \
            "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph"

        # Full, relative path
        g = Graph(path="tests/assets/pylogseq_test_graph")

        assert g.path == \
            "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph"

        # Full, full path
        g = Graph(
            path="/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph"
        )

        assert g.path == \
            "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph"


    # ----------------------------------
    #
    # Get pages from graph. Note that they aren't parsed yet.
    #
    # ----------------------------------
    #@pytest.mark.skip
    def test_get_pages(self):

        g = Graph("tests/assets/pylogseq_test_graph")

        pages = g.get_pages()

        assert [ p.path for p in pages ] == [
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/A.md',
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md',
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/Gestión general.md',
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_pages_folder/page.md',
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/journals/2023_03_30.md'
            ]

        assert [ p.content for p in pages ] == [ None, None, None, None, None ]

        assert [ p.title for p in pages ] == [
            'A', 'a_page_with_a_title', 'Gestión general', 'page', '2023_03_30' ]
