from pylogseq.common import sanitize_path
import os

# ----------------------------------
#
# Tests for the common functions.
#
# ----------------------------------

# ----------------------------------
#
# sanitize_path.
#
# ----------------------------------
class TestCommon:

    def test_sanitize_path(self):
        """Tests the sanitize_path() function.
        """

        # A set of paths to sanitize
        paths: list[str] = [
            "../logseq",
            "../a",
            "//a//b//c//"
        ]

        # Sanitize paths
        sanitized_paths: list[str] = []

        for p in paths:
            sanitized_paths.append(sanitize_path(p))

        # Check the sanitized path
        assert sanitized_paths == [
            "/workspaces/mlktools-pylogseq/src/logseq",
            "/workspaces/mlktools-pylogseq/src/a",
            "//a/b/c"
        ]
