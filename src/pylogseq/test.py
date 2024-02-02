# Small tests to debug with VSC here, check .vscode/launch.json

from pylogseq.page import Page

markdown = """title:: aaa
- #P parent node
- #A child node A
    - #A1 line
    - #A2 line
- #B child node B
"""

p: Page = Page(content=markdown)

b = p.parse(debug=True)

print()

print("D: ", b)
