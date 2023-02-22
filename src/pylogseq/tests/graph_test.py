import os
from pylogseq.graph import Graph

class TestGraph:

    def test_graph(self):
        graph = Graph(os.getcwd())

        assert graph.path == "/workspaces/mlktools-pylogseq/src/pylogseq"
