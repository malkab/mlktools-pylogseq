from pylogseq.page import Page


# ----------------------------------
#
# Individual, quick pytest


# @pytest.mark.skip
class TestParser:
    # ----------------------------------
    #
    # Simple parser test.
    #
    # ----------------------------------
    def test_test(self):
        markdown = """title:: aaa
A Floating line
- #P parent node
  Floating line
- #A child node A
    - #A1 line
    - #A2 line
- #B child node B
"""

        p: Page = Page(content=markdown)

        b = p.parse(debug=True)

        print()

        print("D: ", b)
