import os
from pylogseq.graph import Graph
from pylogseq.page import Page

class TestGraph:

    def test_graph(self):
        graph = Graph("tests/assets/agenda")

        assert graph.path == "tests/assets/agenda"

        graph.get_pages()

        graph.parse()
