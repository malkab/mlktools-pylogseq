import pytest
from pylogseq.mlkgraph.lib.libmlkgraph import get_graphs, process_p_g_i_graph_paths


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
            "./tests/assets/graph_b",
            "./tests/assets/no_es_grafo",
            "./tests/assets/pylogseq_test_graph",
        ]

        # Multiple existing profiles
        p_options = ["profile_a_folder", "profile_b"]

        graphs = process_p_g_i_graph_paths(p_options=p_options)

        assert sorted(graphs) == [
            "./tests/assets/graph_a",
            "./tests/assets/no_es_grafo",
            "./tests/assets/pylogseq_test_graph",
        ]

        # Single -g option
        g_options = ["tests/assets/**"]

        graphs = process_p_g_i_graph_paths(g_options=g_options)

        assert sorted(graphs) == [
            "tests/assets/graph_a",
            "tests/assets/graph_b",
            "tests/assets/no_es_grafo",
            "tests/assets/pylogseq_test_graph",
        ]

        # Multiple -g option
        g_options = [
            "tests/assets/graph_*",
            "tests/assets/pylogseq_test_graph",
        ]

        graphs = process_p_g_i_graph_paths(g_options=g_options)

        assert sorted(graphs) == [
            "tests/assets/graph_a",
            "tests/assets/graph_b",
            "tests/assets/pylogseq_test_graph",
        ]

        # Single -i option
        i_options = ["tests/**"]

        graphs = process_p_g_i_graph_paths(i_options=i_options)

        assert sorted(graphs) == []

        # Multiple -i option
        i_options = ["tests/graph_*", "tests/pylogseq_test_graph"]

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
        g_options = ["tests/assets/graph_*"]

        graphs = process_p_g_i_graph_paths(g_options=g_options)

        assert sorted(graphs) == [
            "tests/assets/graph_a",
            "tests/assets/graph_b",
        ]

        g = get_graphs(graphs)

        assert sorted(g) == [
            "tests/assets/graph_a",
            "tests/assets/graph_b",
        ]
