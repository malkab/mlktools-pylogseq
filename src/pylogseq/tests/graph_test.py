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

        with raises(Exception, match="Can't compute ID for Graph since path is None"):
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

        with raises(Exception, match="Can't compute ID for Graph since path is None"):
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

        with raises(Exception, match="Can't compute ID for Page since path is None"):
            p0.id

        assert p0.path is None

        with raises(Exception, match="Can't compute abs_path for Page since path is None"):
            p0.abs_path

        assert p0.content is None
        assert p0.title is None
        assert p0.graph == g
        assert p0.blocks == []
        assert g.pages == [p0]

        # Init with path
        p1 = g.create_page(path="pages/test_page.md")

        assert p1.id == \
            "ed9d26a61219c158e7b594e84293bd8944c46bb4a0a62e51337e645243185790"
        assert p1.path == "pages/test_page.md"
        assert p1.abs_path == \
            "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/pages/test_page.md"
        assert p1.content is None
        assert p1.title == "test_page"
        assert p1.graph == g
        assert p1.blocks == []
        assert g.pages == [p0, p1]

        # Init with content
        p2 = g.create_page(content="- # Test page")

        with raises(Exception, match="Can't compute ID for Page since path is None"):
            p2.id

        assert p2.path is None

        with raises(Exception, match="Can't compute abs_path for Page since path is None"):
            p2.abs_path

        assert p2.content == "- # Test page"
        assert p2.title is None
        assert p2.graph == g
        assert p2.blocks == []
        assert g.pages == [p0, p1, p2]

        # Init with title
        p3 = g.create_page(title="Test page")

        with raises(Exception, match="Can't compute ID for Page since path is None"):
            p3.id

        assert p3.path is None

        with raises(Exception, match="Can't compute abs_path for Page since path is None"):
            p0.abs_path

        assert p3.content is None
        assert p3.title == "Test page"
        assert p3.graph == g
        assert p3.blocks == []
        assert g.pages == [p0, p1, p2, p3]

        # Full init
        p4 = g.create_page(path="tests/assets/pylogseq_test_graph/pages/test_page.md",
                           content="- # Test page", title="Test page")

        assert p4.id == \
            "4c656219ac9b302421ebf5315384ded4497ae624c809ec9e41039bdec7a25448"
        assert p4.path == \
            "tests/assets/pylogseq_test_graph/pages/test_page.md"
        assert p4.abs_path == \
            "/workspaces/mlktools-pylogseq/src/tests/assets/pylogseq_test_graph/tests/assets/pylogseq_test_graph/pages/test_page.md"
        assert p4.content == "- # Test page"
        assert p4.title == "Test page"
        assert p4.graph == g
        assert p4.blocks == []
        assert g.pages == [p0, p1, p2, p3, p4]


    # ----------------------------------
    #
    # Add page.
    #
    # ----------------------------------
    def test_add_page(self):

        g = Graph(path="tests/assets/pylogseq_test_graph")

        p = Page(path="pages/test_page.md")

        assert g.pages == []
        assert p.graph is None

        g.add_page(p)

        assert g.pages == [ p ]
        assert p.graph == g


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
                'pages/A.md',
                'pages/a_page_with_a_title.md',
                'pages/Gestión general.md',
                'pages/a_pages_folder/page.md',
                'journals/2023_03_30.md'
            ]

        assert [ p.content for p in g.pages ] == [ None, None, None, None, None ]

        assert [ p.title for p in g.pages ] == [
            'A', 'a_page_with_a_title', 'Gestión general', 'page', '2023_03_30' ]

        assert [ p.graph for p in g.pages ] == [ g, g, g, g, g ]


    # ----------------------------------
    #
    # Parse of pages iterator.
    #
    # ----------------------------------
    def test_parse_iter(self):

        g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

        assert g.pages == []

        g.get_pages()

        yield_pages = []

        for page in g.parse_iter():
            yield_pages.append(page)

        assert [ p.path for p in yield_pages ] == [ p.path for p in g.pages ]

        assert [ p.path for p in g.pages ] == [
                'pages/A.md',
                'pages/a_page_with_a_title.md',
                'pages/Gestión general.md',
                'pages/a_pages_folder/page.md',
                'journals/2023_03_30.md'
            ]

        assert [ p.content == None for p in g.pages ] == \
            [ False, False, False, False, False ]

        assert [ p.title for p in g.pages ] == [
                'A',
                'A new title for the test_page set with a "title" property',
                'Gestión general',
                'page',
                '2023_03_30'
            ]

        assert [ p.graph for p in g.pages ] == [ g, g, g, g, g ]

        assert [ p.id for p in g.pages ] == [
                'ad696c15c475b2a1d3ff07448567afd05648edb45905a34ab82f8fc35ccabfa9',
                '4c3c23df51866eef3feea319a845c217f94070007a5001cae0de7a0aed85b6b7',
                'f2129fbf4b8aa322145cf3f8a515b6333cfab09388132850e88f088254682b97',
                'e39040e6e1ca90f861cbcd5d4b0a859594e0c923966214d273497847df7e4a2b',
                '66d0b2be7faa6caa569a0c7e4e0a73962aec3f2e7c8f77d594625a3de9252ddc'
            ]


    # ----------------------------------
    #
    # Parse of pages bulk.
    #
    # ----------------------------------
    def test_parse(self):

        g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

        assert g.pages == []

        g.get_pages()

        g.parse()

        assert [ p.path for p in g.pages ] == [
                'pages/A.md',
                'pages/a_page_with_a_title.md',
                'pages/Gestión general.md',
                'pages/a_pages_folder/page.md',
                'journals/2023_03_30.md'
            ]

        assert [ p.content == None for p in g.pages ] == \
            [ False, False, False, False, False ]

        assert [ p.title for p in g.pages ] == [
                'A',
                'A new title for the test_page set with a "title" property',
                'Gestión general',
                'page',
                '2023_03_30'
            ]

        assert [ p.graph for p in g.pages ] == [ g, g, g, g, g ]

        assert [ p.id for p in g.pages ] == [
                'ad696c15c475b2a1d3ff07448567afd05648edb45905a34ab82f8fc35ccabfa9',
                '4c3c23df51866eef3feea319a845c217f94070007a5001cae0de7a0aed85b6b7',
                'f2129fbf4b8aa322145cf3f8a515b6333cfab09388132850e88f088254682b97',
                'e39040e6e1ca90f861cbcd5d4b0a859594e0c923966214d273497847df7e4a2b',
                '66d0b2be7faa6caa569a0c7e4e0a73962aec3f2e7c8f77d594625a3de9252ddc'
            ]


    # ----------------------------------
    #
    # Get all blocks in graph.
    #
    # ----------------------------------
    def test_get_all_blocks(self):

        g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

        g.get_pages()

        g.parse()

        assert [ b.title for b in g.get_all_blocks() ] == [
                'LATER #Another/tag A block',
                'Do not remove this test page, it is used in [[Python]] tests.',
                'This is a block.',
                'El propósito de esta página es simplemente guardar una tarea **Gestión '
                'general** para todo el grafo. Esta tarea debe estar siempre en estado '
                '**LATER**.',
                'LATER Gestión general #[[Gestión general]] #[[Another/tag]] #T/1',
                'A page in a subfolder.',
                'LATER #Coursera Entrega #T/8',
                'DONE #Reunión Conversación con [[Antonio Cabrera]]'
            ]

        assert [ b.id for b in g.get_all_blocks() ] == [
                '8854c4054f688dfcd930745ed15dfa625f92d78a255b7aef0d253f5420abb949',
                '06b2ad6bc7ec50ac511cc51d0c6844ba17f8ad1cec421c31042f8ef3bf4393b7',
                '4dee743832110aa02ae642831f1a8da503e0a61db7a1bf62fc2fa7d353a7e293',
                '6d864469166e7657296c42969fa30a0377c4f2c076f5b61d60d107785d1bb03c',
                '487b9c2c783b0afef8049f5b447a72a68a1c26f5a620c121f3e95c5f82c937eb',
                '2a773554533302a20c6009021712af174dfc1441aee78b51467bb2c4e8c54e6c',
                '223907ab91b2060ee92cf7cfab16b7f25fb1000db912c1723c4d6f83999224f9',
                '6ed90f3510b87be9f16506e4d846f99e745b8cf4629d3a80ee13346a8e83105e'
            ]


    # ----------------------------------
    #
    # Check the ID of pages and blocks change with the ID of the graph.
    #
    # ----------------------------------
    def test_change_id(self):

        g = Graph("pylogseq/tests/assets/pylogseq_test_graph")

        g.get_pages()

        g.parse()

        assert g.id == \
            "45f7e878af560d4b64a418707c3fcdb6cb92aaabf22a74cd609e1b3fd2764bae"

        assert [ p.id for p in g.pages ] == [
                'ad696c15c475b2a1d3ff07448567afd05648edb45905a34ab82f8fc35ccabfa9',
                '4c3c23df51866eef3feea319a845c217f94070007a5001cae0de7a0aed85b6b7',
                'f2129fbf4b8aa322145cf3f8a515b6333cfab09388132850e88f088254682b97',
                'e39040e6e1ca90f861cbcd5d4b0a859594e0c923966214d273497847df7e4a2b',
                '66d0b2be7faa6caa569a0c7e4e0a73962aec3f2e7c8f77d594625a3de9252ddc'
            ]

        assert [ b.id for b in g.get_all_blocks() ] == [
                '8854c4054f688dfcd930745ed15dfa625f92d78a255b7aef0d253f5420abb949',
                '06b2ad6bc7ec50ac511cc51d0c6844ba17f8ad1cec421c31042f8ef3bf4393b7',
                '4dee743832110aa02ae642831f1a8da503e0a61db7a1bf62fc2fa7d353a7e293',
                '6d864469166e7657296c42969fa30a0377c4f2c076f5b61d60d107785d1bb03c',
                '487b9c2c783b0afef8049f5b447a72a68a1c26f5a620c121f3e95c5f82c937eb',
                '2a773554533302a20c6009021712af174dfc1441aee78b51467bb2c4e8c54e6c',
                '223907ab91b2060ee92cf7cfab16b7f25fb1000db912c1723c4d6f83999224f9',
                '6ed90f3510b87be9f16506e4d846f99e745b8cf4629d3a80ee13346a8e83105e'
            ]

        # Change the ID
        g.path = "a/new/path"

        assert g.id == \
            "bcf099770d6e5d419a6dcd3c4b7c9de80c01bfa921e8b9cab4d65aeff6100584"

        assert [ p.id for p in g.pages ] == [
                'f183f3e3afa9a80717e8cb205433a8d4a3f363069b75ef31f24eee5dd31b90c4',
                '654642594d76ec69780cb8fb4991a82522988adc87e2ee8995a7e3fc9bdb1f38',
                '353f464dbaf718d0bd171b25517dd1e4b0c5fdd5e2dcb7e00b52c7982c0a86f5',
                '7b48d0840d184ea6cd9c223b39d23884eb5527d133fe831f46c1ed3800891d5e',
                'f55d236f8e771365ecd13074c1faad3458ab3c8cdd13729a34ad3d89882a9b77'
            ]

        assert [ b.id for b in g.get_all_blocks() ] == [
                'bcc6443a5d10cc42f0b59fece1611cd3293a3147da3dde807fc7d60105f6ef26',
                '21d494417ad4cc66939f091c75c0c9c11449d8333542c8dd90e9b274dda89532',
                'bc9d156d677bcf81ed81581d9a65aa1aba4473a3486c4b03cbfb43e61ab54a87',
                '57d05e909bc8a2a1475776736076ccdd55da665db73d4197e4baba27c8ce9d78',
                'c518f4c9bcc1cb1a960e2329462c65bed47f5e07d051f666535a63cf28461c7a',
                '1139856c7f693350e4a977765f32273fca6ea7bb0e5c7ad0a334c438eaae91cd',
                'c7d009617f35239d6c38e5beabe4d0dc34e51ea1b47d8d09996ff04fe42f25c1',
                'bfe84ce50945d9d85f599b0327337071fd9e30590da41e4bca8d3b617464b396'
            ]
