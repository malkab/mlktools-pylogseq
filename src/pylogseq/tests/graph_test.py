from pylogseq.graph import Graph
from pylogseq.page import Page
from pytest import raises

class TestGraph:

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def test_graph_constructor(self):

        # Bare constructor
        g = Graph()

        assert g.path is None

        with raises(Exception, match="Graph has no path, cannot generate ID."):
            g.id

        assert g.title is None

        assert g.pages == []

        # Optional path
        g = Graph(path="tests/assets/pylogseq_test_graph")

        assert g.path == \
            "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph"

        assert g.id == \
            "5c9465e284e91f4f0bbce4238e6f3b86aaf689e08543b0d79aaeafc3bb5b01b2"

        assert g.title == "pylogseq_test_graph"

        assert g.pages == []

        # Optional title
        g = Graph(title="test_graph")

        assert g.path is None

        with raises(Exception, match="Graph has no path, cannot generate ID."):
            g.id

        assert g.title == "test_graph"

        assert g.pages == []

        # Full, relative path
        g = Graph(path="tests/assets/pylogseq_test_graph", title="test_graph")

        assert g.path == \
            "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph"

        assert g.id == \
            "5c9465e284e91f4f0bbce4238e6f3b86aaf689e08543b0d79aaeafc3bb5b01b2"

        assert g.title == "test_graph"

        assert g.pages == []

        # Full, full path
        g = Graph(
            path="/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph",
            title="test_graph"
        )

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

        g = Graph(path="tests/assets/pylogseq_test_graph")

        # Bare factory
        p0 = g.create_page()

        with raises(Exception, match="Page has no path and/or page's graph has no ID, cannot generate ID"):
            p0.id

        with raises(Exception, match="Page has no path and/or page's graph has no path, cannot generate absolute path."):
            p0.abs_path

        assert p0.path is None
        assert p0.content is None
        assert p0.title is None
        assert p0.graph == g
        assert p0.blocks == []
        assert g.pages == [p0]

        # Init with path
        p1 = g.create_page(path="pages/test_page.md")

        assert p1.path == "pages/test_page.md"
        assert p1.abs_path == \
            "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/test_page.md"
        assert p1.content is None
        assert p1.title == "test_page"
        assert p1.graph == g
        assert p1.blocks == []
        assert p1.id == \
            "ed9d26a61219c158e7b594e84293bd8944c46bb4a0a62e51337e645243185790"
        assert g.pages == [p0, p1]

        # # Init with content
        # p2 = g.create_page(PAGETYPE.PAGE, content="- # Test page")

        # with raises(Exception, match="Page has no path and/or page's graph has no ID, cannot generate ID"):
        #     p2.id

        # assert p2.path is None
        # assert p2.content == "- # Test page"
        # assert p2.title is None
        # assert p2.graph == g
        # assert p2.blocks == []
        # assert g.pages == [p0, p1, p2]

        # # Init with title
        # p3 = g.create_page(PAGETYPE.PAGE, title="Test page")

        # with raises(Exception, match="Page has no path and/or page's graph has no ID, cannot generate ID"):
        #     p3.id

        # assert p3.path is None
        # assert p3.content is None
        # assert p3.title == "Test page"
        # assert p3.graph == g
        # assert p3.blocks == []
        # assert g.pages == [p0, p1, p2, p3]

        # # Full init
        # p4 = g.create_page(PAGETYPE.PAGE, path="tests/assets/pylogseq_test_graph/pages/test_page.md",
        #                    content="- # Test page", title="Test page")

        # assert p4.path == "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/test_page.md"
        # assert p4.content == "- # Test page"
        # assert p4.title == "Test page"
        # assert p4.graph == g
        # assert p4.blocks == []
        # assert p4.id == "4c20bf164120d647109f663efaf37b0bf8a0bdd2031bf0572b02eebc8a2d5c23"
        # assert g.pages == [p0, p1, p2, p3, p4]


    # # ----------------------------------
    # #
    # # Get pages from graph. Note that they aren't parsed yet.
    # #
    # # ----------------------------------
    # def test_get_pages(self):

    #     g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

    #     assert g.pages == []

    #     g.get_pages()

    #     assert [ p.path for p in g.pages ] == [
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/A.md',
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md',
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/Gestión general.md',
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/journals/2023_03_30.md'
    #         ]

    #     assert [ p.content for p in g.pages ] == [ None, None, None, None ]

    #     assert [ p.title for p in g.pages ] == [
    #         'A', 'a_page_with_a_title', 'Gestión general', '2023_03_30' ]

    #     assert [ p.graph for p in g.pages ] == [ g, g, g, g ]


    # # ----------------------------------
    # #
    # # Parse of pages iterator.
    # #
    # # ----------------------------------
    # def test_parse_iter(self):

    #     g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

    #     assert g.pages == []

    #     g.get_pages()

    #     yield_pages = []

    #     for page in g.parse_iter():
    #         yield_pages.append(page)

    #     assert [ p.path for p in yield_pages ] == [ p.path for p in g.pages ]

    #     assert [ p.path for p in g.pages ] == [
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/A.md',
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md',
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/Gestión general.md',
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/journals/2023_03_30.md'
    #         ]

    #     assert [ p.content == None for p in g.pages ] == [ False, False, False, False ]

    #     assert [ p.title for p in g.pages ] == [
    #         'A', 'A new title for the test_page set with a "title" property',
    #         'Gestión general', '2023_03_30' ]

    #     assert [ p.graph for p in g.pages ] == [ g, g, g, g ]

    #     assert [ p.id for p in g.pages ] == [
    #         '55714fe9a0801415521b240dc1da14ab911104b4e57768c085e4c9b27efc0a1b',
    #         'd2a8918f9d2f71a17e0762549f0d4f4dbf2aaeb6cf8bd7eaeb8ec00108406931',
    #         '6dee4011ab23c45b3950d4a289ba582815350017b40f23ed6acc4a15afa2c18c',
    #         '89bf2ffa22bc291b50a69116004dd7409dd7317f8426102a65a7054528f77f05'
    #     ]


    # # ----------------------------------
    # #
    # # Parse of pages bulk.
    # #
    # # ----------------------------------
    # def test_parse(self):

    #     g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

    #     assert g.pages == []

    #     g.get_pages()

    #     g.parse()

    #     assert [ p.path for p in g.pages ] == [
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/A.md',
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/a_page_with_a_title.md',
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/pages/Gestión general.md',
    #             '/workspaces/mlktools-pylogseq/src/pylogseq/tests/assets/pylogseq_test_graph/journals/2023_03_30.md'
    #         ]

    #     assert [ p.content == None for p in g.pages ] == [ False, False, False, False ]

    #     assert [ p.title for p in g.pages ] == [
    #         'A', 'A new title for the test_page set with a "title" property',
    #         'Gestión general', '2023_03_30' ]

    #     assert [ p.graph for p in g.pages ] == [ g, g, g, g ]

    #     assert [ p.id for p in g.pages ] == [
    #         '55714fe9a0801415521b240dc1da14ab911104b4e57768c085e4c9b27efc0a1b',
    #         'd2a8918f9d2f71a17e0762549f0d4f4dbf2aaeb6cf8bd7eaeb8ec00108406931',
    #         '6dee4011ab23c45b3950d4a289ba582815350017b40f23ed6acc4a15afa2c18c',
    #         '89bf2ffa22bc291b50a69116004dd7409dd7317f8426102a65a7054528f77f05'
    #     ]


    # # ----------------------------------
    # #
    # # Get all blocks in graph.
    # #
    # # ----------------------------------
    # def test_get_all_blocks(self):

    #     g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

    #     g.get_pages()

    #     g.parse()

    #     assert [ b.title for b in g.get_all_blocks() ] == [
    #         'LATER #Another/tag A block',
    #         'Do not remove this test page, it is used in [[Python]] tests.',
    #         'This is a block.',
    #         'El propósito de esta página es simplemente guardar una tarea **Gestión '
    #         'general** para todo el grafo. Esta tarea debe estar siempre en estado '
    #         '**LATER**.',
    #         'LATER Gestión general #[[Gestión general]] #[[Another/tag]] #T/1',
    #         'LATER #Coursera Entrega #T/8',
    #         'DONE #Reunión Conversación con [[Antonio Cabrera]]'
    #     ]

    #     assert [ b.id for b in g.get_all_blocks() ] == [
    #         '6b90b523e6642c35d37340e133ccbbe03e257d1177d954f6227d9a76377fcc51',
    #         'bc23191222d6b5e90ed4a69374a41e2f9f1671e0622171bc5bb3709d2108fd98',
    #         '64b4a706fe714e8deba37d1bc7d23bdfdf6fbdc85a6160213739b452bb105001',
    #         '5a7fa3e2eb33cc8ea6895d5da7a294739beac33bfb16c029be85a83cd02f1bdb',
    #         'a058f8a047ec1efd42c894c638701feeabbda783974c50fc00a1dff256e22591',
    #         'd303b8c7be73d7d9f79ce7fdc4ace64d04a6ec91dd740c22d50b22d408d55f37',
    #         'ede8dbf654570c48bad89d0dfd0a7392455695cf20e25bcbbf6c69d2485eeb96'
    #     ]


    # # ----------------------------------
    # #
    # # Check the ID of pages and blocks change with the ID of the graph.
    # #
    # # ----------------------------------
    # def test_change_id(self):

    #     g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

    #     g.get_pages()

    #     g.parse()

    #     assert g.id == \
    #         "45f7e878af560d4b64a418707c3fcdb6cb92aaabf22a74cd609e1b3fd2764bae"

    #     assert [ p.id for p in g.pages ] == [
    #         '55714fe9a0801415521b240dc1da14ab911104b4e57768c085e4c9b27efc0a1b',
    #         'd2a8918f9d2f71a17e0762549f0d4f4dbf2aaeb6cf8bd7eaeb8ec00108406931',
    #         '6dee4011ab23c45b3950d4a289ba582815350017b40f23ed6acc4a15afa2c18c',
    #         '89bf2ffa22bc291b50a69116004dd7409dd7317f8426102a65a7054528f77f05'
    #     ]

    #     assert [ b.id for b in g.get_all_blocks() ] == [
    #         '6b90b523e6642c35d37340e133ccbbe03e257d1177d954f6227d9a76377fcc51',
    #         'bc23191222d6b5e90ed4a69374a41e2f9f1671e0622171bc5bb3709d2108fd98',
    #         '64b4a706fe714e8deba37d1bc7d23bdfdf6fbdc85a6160213739b452bb105001',
    #         '5a7fa3e2eb33cc8ea6895d5da7a294739beac33bfb16c029be85a83cd02f1bdb',
    #         'a058f8a047ec1efd42c894c638701feeabbda783974c50fc00a1dff256e22591',
    #         'd303b8c7be73d7d9f79ce7fdc4ace64d04a6ec91dd740c22d50b22d408d55f37',
    #         'ede8dbf654570c48bad89d0dfd0a7392455695cf20e25bcbbf6c69d2485eeb96'
    #     ]

    #     # Change the ID
    #     g.path = "a/new/path"

    #     assert g.id == \
    #         "bcf099770d6e5d419a6dcd3c4b7c9de80c01bfa921e8b9cab4d65aeff6100584"

    #     assert [ p.id for p in g.pages ] == [
    #         '55714fe9a0801415521b240dc1da14ab911104b4e57768c085e4c9b27efc0a1b',
    #         'd2a8918f9d2f71a17e0762549f0d4f4dbf2aaeb6cf8bd7eaeb8ec00108406931',
    #         '6dee4011ab23c45b3950d4a289ba582815350017b40f23ed6acc4a15afa2c18c',
    #         '89bf2ffa22bc291b50a69116004dd7409dd7317f8426102a65a7054528f77f05'
    #     ]

    #     assert [ b.id for b in g.get_all_blocks() ] == [
    #         '6b90b523e6642c35d37340e133ccbbe03e257d1177d954f6227d9a76377fcc51',
    #         'bc23191222d6b5e90ed4a69374a41e2f9f1671e0622171bc5bb3709d2108fd98',
    #         '64b4a706fe714e8deba37d1bc7d23bdfdf6fbdc85a6160213739b452bb105001',
    #         '5a7fa3e2eb33cc8ea6895d5da7a294739beac33bfb16c029be85a83cd02f1bdb',
    #         'a058f8a047ec1efd42c894c638701feeabbda783974c50fc00a1dff256e22591',
    #         'd303b8c7be73d7d9f79ce7fdc4ace64d04a6ec91dd740c22d50b22d408d55f37',
    #         'ede8dbf654570c48bad89d0dfd0a7392455695cf20e25bcbbf6c69d2485eeb96'
    #     ]
