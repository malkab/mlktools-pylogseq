from pylogseq.graph import Graph

class TestGraph:

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def test_graph_constructor(self):

        # Bare constructor
        g = Graph("tests/assets/pylogseq_test_graph")

        assert g.path == \
            "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph"

        assert g.id == \
            "45f7e878af560d4b64a418707c3fcdb6cb92aaabf22a74cd609e1b3fd2764bae"

        assert g.title == "pylogseq_test_graph"

        assert g.pages_file_name == []

        assert g.pages == []

        # Optional title
        g = Graph("tests/assets/pylogseq_test_graph", title="test_graph")

        assert g.path == \
            "/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph"

        assert g.id == \
            "45f7e878af560d4b64a418707c3fcdb6cb92aaabf22a74cd609e1b3fd2764bae"

        assert g.title == "test_graph"

        assert g.pages_file_name == []

        assert g.pages == []


    # ----------------------------------
    #
    # Parse of pages.
    #
    # ----------------------------------
    def test_parse(self):
        g = Graph("tests/assets/pylogseq_test_graph")

        assert g.pages_file_name == []

        assert g.pages == []

        g.get_pages()

        assert g.pages_file_name == [
            '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/A.md',
            '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md',
            '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/Gestión general.md',
            '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/journals/2023_03_30.md'
        ]

        assert g.pages == []

        # To store resulting page's titles
        page_title: list[str] = []

        for p in g.parse():
            page_title.append(p.title)

        assert len(g.pages) == 4
        assert g.pages[0].graph.title == "pylogseq_test_graph"

        assert page_title == [
            'A',
            'A new title for the test_page set with a "title" property',
            'Gestión general',
            '2023_03_30'
        ]
