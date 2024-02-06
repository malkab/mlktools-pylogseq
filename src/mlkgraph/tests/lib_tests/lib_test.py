import pytest
from mlkgraph.lib.libmlkgraph import get_graphs, process_p_g_i_graph_paths


# @pytest.mark.skip
class TestLib:
    # ----------------------------------
    #
    # Test process_p_g_i_graph_paths method.
    #
    # ----------------------------------
    def test_process_p_g_i_graph_paths(self):
        """Test constructor and initial members status."""

        # Empty run
        graphs = process_p_g_i_graph_paths()

        assert sorted(graphs) == []

        # Non-existing profile
        p_options: list[str] = ["a"]

        with pytest.raises(Exception) as e:
            process_p_g_i_graph_paths(p_options=p_options)

            assert e.value == "Profile a not found"

        # Single existing profile
        p_options = ["profile_a_folder"]

        graphs = process_p_g_i_graph_paths(p_options=p_options)

        assert sorted(graphs) == [
            "./tests/mlkgraph_tests/graph_b",
            "./tests/mlkgraph_tests/no_es_grafo",
            "./tests/mlkgraph_tests/pylogseq_test_graph",
        ]

        # Multiple existing profiles
        p_options = ["profile_a_folder", "profile_b"]

        graphs = process_p_g_i_graph_paths(p_options=p_options)

        assert sorted(graphs) == [
            "./tests/mlkgraph_tests/graph_a",
            "./tests/mlkgraph_tests/no_es_grafo",
            "./tests/mlkgraph_tests/pylogseq_test_graph",
        ]

        # Single -g option
        g_options = ["tests/mlkgraph_tests/**"]

        graphs = process_p_g_i_graph_paths(g_options=g_options)

        assert sorted(graphs) == [
            "tests/mlkgraph_tests/graph_a",
            "tests/mlkgraph_tests/graph_b",
            "tests/mlkgraph_tests/no_es_grafo",
            "tests/mlkgraph_tests/pylogseq_test_graph",
        ]

        # Multiple -g option
        g_options = [
            "tests/mlkgraph_tests/graph_*",
            "tests/mlkgraph_tests/pylogseq_test_graph",
        ]

        graphs = process_p_g_i_graph_paths(g_options=g_options)

        assert sorted(graphs) == [
            "tests/mlkgraph_tests/graph_a",
            "tests/mlkgraph_tests/graph_b",
            "tests/mlkgraph_tests/pylogseq_test_graph",
        ]

        # Single -i option
        i_options = ["mlkgraph_tests/**"]

        graphs = process_p_g_i_graph_paths(i_options=i_options)

        assert sorted(graphs) == []

        # Multiple -i option
        i_options = ["mlkgraph_tests/graph_*", "mlkgraph_tests/pylogseq_test_graph"]

        graphs = process_p_g_i_graph_paths(i_options=i_options)

        assert sorted(graphs) == []

    # ----------------------
    #
    # Test the get_graphs method.
    #
    # ----------------------
    def test_get_graphs(self):
        """Tests the get_graphs method."""

        # Get graphs
        g_options = ["tests/mlkgraph_tests/graph_*"]

        graphs = process_p_g_i_graph_paths(g_options=g_options)

        assert sorted(graphs) == [
            "tests/mlkgraph_tests/graph_a",
            "tests/mlkgraph_tests/graph_b",
        ]

        g = get_graphs(graphs)

        assert sorted(g) == [
            "tests/mlkgraph_tests/graph_a",
            "tests/mlkgraph_tests/graph_b",
        ]
