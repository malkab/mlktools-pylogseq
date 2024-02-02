from marko import Markdown
from marko.block import Document
from pylogseq.mdlogseq.logseqparse import LogseqParse

# TODO: DOCUMENT


class Parser:
    """This is the parser class. It parses markdown that contains specific
    Logseq syntax and returns a tree of parsed objects.
    """

    def parse(self, markdown: str) -> Document:
        """Parses a Markdown string and returns a tree of parsed objects.

        Args:
            markdown (str): The Markdown string to parse.

        Returns:
            marko.block.Document:
                This type has several critical members, being the most important one
                children, where the parsed tree is stored.
        """
        parser = Markdown(extensions=[LogseqParse])  # type: ignore

        return parser.parse(markdown)
