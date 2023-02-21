import sys
import os
sys.path.insert(0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import pytest

from pylogseq.graph import Graph

class TestGraph:

    def test_graph(self):
        graph = Graph(os.getcwd())

        assert graph.path == "/workspaces/mlktools-pylogseq/src/pylogseq/tests"
