import os
from pylogseq.graph import Graph
from pylogseq.page import Page

class TestGraph:

    def test_graph(self):
        graph = Graph("tests/assets/Agenda")

        assert graph.path == "tests/assets/Agenda"

        graph.get_md_pages()

        graph.read_pages()

        print("D: uuu", graph.pages)
