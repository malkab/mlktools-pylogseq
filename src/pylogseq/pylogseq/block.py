"""This class takes a top block (the ones starting by "- " in text read from a
Logseq page and parses it into Markdown, analyzing everything.
"""

import marko
from typing import Any
import hashlib
from .parser import Parser
import pylogseq


class Block():
    """A class to represent a top level block.

    Attributes:
        tags (list[str]):
            List of unique tags found in the block.
        content (str):
            Sanitized content of the block, in plain str, suitable for moving.
        content_hash (str):
            The hash of the sanitized content.
        highest_priority (str):
            The highest priority found in the block.
        done (bool):
            Is the block marked as done?
        later (bool):
            Is the block marked as later?
        now (bool):
            Is the block marked as now?
        words (list[str]):
            List of unique words found in the block (subject to exclusion).
        priorities (list[str]):
            Unique priorities found in the block.
        logbook (list[Any]):
            List of LogBook entries found in the block.
        excluded_words (list[str]):
            The list of excluded words for finding unquiue words.

    Raises:
        Exception: _description_
    """


    def __init__(self, content: str, excluded_words: list[str]=[]):
        """Constructor.

        Args:
            content (str):
                The block's content in a plain str. This will be parsed by the
                Markdown parser.
            excluded_words (list[str], optional):
                List of words to filter in the list of unique words. Defaults to
                [].
        """
        self.tags: list[str] = []
        self.content: str = content.strip("\n").strip()
        self.content_hash: str = hashlib.sha256(content.encode()).hexdigest()
        self.highest_priority: str = None
        self.done: bool = False
        self.later: bool = False
        self.now: bool = False
        self.words: list[str] = []
        self.priorities: list[str] = []
        self.logbook: list[Any] = []
        self.excluded_words = excluded_words

        # Parse the content
        p = Parser()
        self.process(p.parse(self.content))

        # Postprocess data
        self.priorities = sorted(list(set(self.priorities)))
        self.tags = sorted(list(set(self.tags)))

        if len(self.priorities) > 0:
            self.highest_priority = self.priorities[0]

        self.words = sorted(list(set(self.words)))


    def process(self, item: Any) -> None:
        """Process the block from a ListItem (a Logseq block) found in the
        parsing of the Markdown of a Logseq page.

        Args:
            item (Any):
                A Markdown parsed object.

        Raises:
            Exception:
                Raises an exception if a type of block item is unprocessable.
        """
        if \
            isinstance(item, marko.block.Document) or \
            isinstance(item, marko.block.List) or \
            isinstance(item, marko.block.ListItem) or \
            isinstance(item, marko.block.Paragraph) or \
            isinstance(item, marko.block.FencedCode) or \
            isinstance(item, marko.block.Heading) or \
            isinstance(item, marko.inline.StrongEmphasis): \

            for child in item.children:
                self.process(child)

        elif isinstance(item, pylogseq.mdlogseq.elements_parsers.logseqdoneclass.LogseqDone):

            self.done = True

        elif isinstance(item, marko.inline.RawText):

            self.words.extend(self._process_words(item.children, self.excluded_words))

        elif isinstance(item, pylogseq.mdlogseq.elements_parsers.LogseqPriority):

            self.priorities.append(item.target)

        elif isinstance(item, pylogseq.mdlogseq.elements_parsers.logseqclockclass.LogseqClock):

            self.logbook.append(item.target)

        elif isinstance(item, pylogseq.mdlogseq.elements_parsers.logseqlaterclass.LogseqLater):

            self.later = True

        elif isinstance(item, pylogseq.mdlogseq.elements_parsers.logseqnowclass.LogseqNow):

            self.now = True

        elif \
            isinstance(item, pylogseq.mdlogseq.elements_parsers.LogseqTag) or \
            isinstance(item, pylogseq.mdlogseq.elements_parsers.LogseqComposedTag) or \
            isinstance(item, pylogseq.mdlogseq.elements_parsers.LogseqSquareTag):

            self.tags.extend(item.target)

        elif \
            isinstance(item, marko.inline.LineBreak) or \
            isinstance(item, marko.block.BlankLine) or \
            isinstance(item, pylogseq.mdlogseq.elements_parsers.logseqlogbookclass.LogseqLogBook) or \
            isinstance(item, pylogseq.mdlogseq.elements_parsers.logseqendclass.LogseqEnd):

            pass

        else:
            if hasattr(item, "target"):
                target = item.target
            else:
                target = None

            if hasattr(item, "children"):
                children = item.children
            else:
                children = None

            raise Exception(f"Unknown item while processing Block: type {type(item)}, target {target}, children {children}")


    def _process_words(self, text: str, excluded_words: list[str] = []) -> list[str]:
        """Process text, sanitizes it, and returns a list of unique words, with
        optional exclusion.

        Args:
            text (str):
                The text to process.
            excluded_words (list[str], optional):
                A list of excluded words. Defaults to [].

        Returns:
            list[str]:
                The list of unique words found.
        """
        t: list[str] = text.split(" ")

        t = map(lambda x: x \
            .lower() \
            .replace("(", "") \
            .replace(")", "") \
            .lstrip(".") \
            .rstrip(".") \
            .lstrip(",") \
            .rstrip(","), t)

        return filter(lambda x: x != "" and x not in excluded_words, t)
