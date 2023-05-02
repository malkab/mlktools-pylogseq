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
            "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph"

        assert g.id == \
            "5c9465e284e91f4f0bbce4238e6f3b86aaf689e08543b0d79aaeafc3bb5b01b2"

        assert g.title == "pylogseq_test_graph"

        assert g.pages == []

        # Optional title
        g = Graph("tests/assets/pylogseq_test_graph", title="test_graph")

        assert g.path == \
            "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph"

        assert g.id == \
            "5c9465e284e91f4f0bbce4238e6f3b86aaf689e08543b0d79aaeafc3bb5b01b2"

        assert g.title == "test_graph"

        assert g.pages == []


    # ----------------------------------
    #
    # Page factory.
    #
    # ----------------------------------
    def test_page_factory(self):

        g = Graph("tests/assets/pylogseq_test_graph")

        # Bare factory
        p0 = g.create_page()

        assert p0.path is None
        assert p0.content is None
        assert p0.title is None
        assert p0.graph == g
        assert p0.blocks == []
        assert p0.id is None
        assert g.pages == [p0]

        # Init with path
        p1 = g.create_page(path="tests/assets/pylogseq_test_graph/pages/test_page.md")

        assert p1.path == "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/test_page.md"
        assert p1.content is None
        assert p1.title == "test_page"
        assert p1.graph == g
        assert p1.blocks == []
        assert p1.id == "df7b27ca8cd75e82ec20a644752f96d7c63f913bf4e4d18246f95abb1b9d8e14"
        assert g.pages == [p0, p1]

        # Init with content
        p2 = g.create_page(content="- # Test page")

        assert p2.path is None
        assert p2.content == "- # Test page"
        assert p2.title is None
        assert p2.graph == g
        assert p2.blocks == []
        assert p2.id is None
        assert g.pages == [p0, p1, p2]

        # Init with title
        p3 = g.create_page(title="Test page")

        assert p3.path is None
        assert p3.content is None
        assert p3.title == "Test page"
        assert p3.graph == g
        assert p3.blocks == []
        assert p3.id is None
        assert g.pages == [p0, p1, p2, p3]

        # Full init
        p4 = g.create_page(path="tests/assets/pylogseq_test_graph/pages/test_page.md",
                           content="- # Test page", title="Test page")

        assert p4.path == "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/test_page.md"
        assert p4.content == "- # Test page"
        assert p4.title == "Test page"
        assert p4.graph == g
        assert p4.blocks == []
        assert p4.id == "df7b27ca8cd75e82ec20a644752f96d7c63f913bf4e4d18246f95abb1b9d8e14"
        assert g.pages == [p0, p1, p2, p3, p4]


    # ----------------------------------
    #
    # Get pages from graph. Note that they aren't parsed yet.
    #
    # ----------------------------------
    def test_get_pages(self):

        g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

        assert g.pages == []

        g.get_pages()

        assert [ p.path for p in g.pages ] == [
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/A.md',
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md',
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/Gestión general.md',
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/journals/2023_03_30.md'
            ]

        assert [ p.content for p in g.pages ] == [ None, None, None, None ]

        assert [ p.title for p in g.pages ] == [
            'A', 'a_page_with_a_title', 'Gestión general', '2023_03_30' ]

        assert [ p.graph for p in g.pages ] == [ g, g, g, g ]


    # ----------------------------------
    #
    # Parse of pages.
    #
    # ----------------------------------
    def test_parse(self):

        g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

        assert g.pages == []

        g.get_pages()

        g.parse()

        assert [ p.path for p in g.pages ] == [
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/A.md',
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md',
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/Gestión general.md',
                '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/journals/2023_03_30.md'
            ]

        assert [ p.content for p in g.pages ] == [ None, None, None, None ]

        assert [ p.title for p in g.pages ] == [
            'A', 'a_page_with_a_title', 'Gestión general', '2023_03_30' ]

        assert [ p.graph for p in g.pages ] == [ g, g, g, g ]
