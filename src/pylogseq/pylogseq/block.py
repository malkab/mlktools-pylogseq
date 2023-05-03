"""This class takes a top block (the ones starting by "- " in text read from a
Logseq page and parses it into Markdown, analyzing everything.
"""

import marko
import datetime
from typing import Any
import hashlib
from common import sanitize_content
from .parser import Parser
from .forward_declarations import ClockBlock, Page
from .mdlogseq.elements_parsers.logseqdoneclass import LogseqDone
from .mdlogseq.elements_parsers.logseqpriorityclass import LogseqPriority
from .mdlogseq.elements_parsers.logseqclockclass import LogseqClock
from .mdlogseq.elements_parsers.logseqlaterclass import LogseqLater
from .mdlogseq.elements_parsers.logseqnowclass import LogseqNow
from .mdlogseq.elements_parsers import LogseqTag
from .mdlogseq.elements_parsers import LogseqComposedTag
from .mdlogseq.elements_parsers import LogseqSquareTag
from .mdlogseq.elements_parsers.logseqlogbookclass import LogseqLogBook
from .mdlogseq.elements_parsers.logseqendclass import LogseqEnd
from .mdlogseq.elements_parsers.logseqscheduledclass import LogseqScheduled
from .mdlogseq.elements_parsers.logseqdeadlineclass import LogseqDeadline

# ----------------------------------
#
# dd
#
# ----------------------------------
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

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def __init__(self, content: str=None, page: Page=None,
                 order_in_page: int=None):
        """Constructor.

        Args:
            content (str):
                The block's content in a plain str. This will be parsed by the
                Markdown parser.
            excluded_words (list[str], optional):
                List of words to filter in the list of unique words. Defaults to
                [].
        """
        from .page import Page

        self.content: str = sanitize_content(content) if content else None
        """Sanitized content of the block. Content for a block must start with '- '.
        """

        self.page: Page = page
        """The page this block belongs to.
        """

        self.order_in_page = order_in_page
        """The order in the page this block is in.
        """

        self.tags: list[str] = []
        """List of unique tags found in the block.
        """

        self.highest_priority: str = None
        """The highest priority found in the block.
        """

        self.done: bool = False
        """Flag to signal that the block is marked as done.
        """

        self.later: bool = False
        """Flag to signal that the block is marked as later.
        """

        self.now: bool = False
        """Flag to signal that the block is marked as now.
        """

        self.priorities: list[str] = []
        """Unique priorities found in the block.
        """

        self.logbook: list[Any] = []
        """List of LogBook entries found in the block.
        """

        self.allocated_time: int = None
        """The allocated time for the block found in T tags.
        """

        self.scheduled: datetime.datetime = None
        """The scheduled date for the block.
        """

        self.deadline: datetime.datetime = None
        """The deadline date for the block.
        """

        self.elapsed_time: datetime.timedelta = None
        """The elapsed time for the block as the sum of the logbook entries.
        """

        self.time_left: datetime.timedelta = None
        """The time left for the block as the difference between the allocated
        time and the sum of the elapsed times in logbook entries.
        """

        self.title: str = content.split("\n")[0].strip("- ").strip() if content \
            else None
        """The title of the block, the first line of the content, without '-'.
        """


    # ----------------------------------
    #
    # Property id.
    # ID of the block.
    #
    # ----------------------------------
    @property
    def id(self) -> str:
        """The hashed ID. It depends on the path of the parent page and the
        content of the block.
        """
        if self.content is None:
            raise Exception("Can't compute ID for Block since content is None")

        if self.order_in_page is None:
            raise Exception("Can't compute ID for Block since order_in_page is None")

        try:
            hash = f"{self.page.id}{self.content}{self.order_in_page}"
            hash = hashlib.sha256(hash.encode())
            return hash.hexdigest()
        except(Exception) as e:
            raise Exception(f"Can't compute ID for Block: check parent page exists and that has a valid ID")


    # ----------------------------------
    #
    # Parse the block content.
    #
    # ----------------------------------
    def parse(self) -> None:
        """Parses the block's content by initiating the recursive parsing of
        anidated blocks.

        Raises:
            Exception: Raises an exception if the block's content is empty.
            Exception: Raises an exception if the allocated time in T tags
                cannot be processed.
        """

        if not self.content:
            raise Exception("Block content is empty.")

        # Parse the content
        p = Parser()

        # Start the recursive processing of the parsed content
        self._process(p.parse(self.content))

        # Postprocess data
        self.priorities = sorted(list(set(self.priorities)))
        self.tags = sorted(list(set(self.tags)))

        # Check for highest priority
        if len(self.priorities) > 0:
            self.highest_priority = self.priorities[0]

        # Check if there is an allocated time tag T
        if "T" in self.tags:

            time_tag = list(filter(lambda x: x.startswith("T/"), self.tags))[0]

            try:
                time_tag = int(time_tag.strip("T/"))
                self.allocated_time = datetime.timedelta(hours=time_tag)

                # Check if there is are clocked time
                if self.elapsed_time is not None:
                    self.time_left = self.allocated_time - self.elapsed_time
            except:
                raise Exception("Invalid allocated time tag: " + time_tag)


    # ----------------------------------
    #
    # Recursive function to process the block's content.
    #
    # ----------------------------------
    def _process(self, item: Any) -> None:
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
                self._process(child)

        elif isinstance(item, LogseqDone):
            self.done = True

        elif isinstance(item, marko.inline.RawText):
            pass

        elif isinstance(item, LogseqPriority):
            self.priorities.append(item.target)

        elif isinstance(item, LogseqClock):
            for clock in item.target:
                if self.elapsed_time is None:
                    self.elapsed_time = clock.elapsed_time
                else:
                    self.elapsed_time += clock.elapsed_time

            self.logbook.extend(item.target)

        elif isinstance(item, LogseqLater):
            self.later = True

        elif isinstance(item, LogseqNow):
            self.now = True

        elif \
            isinstance(item, LogseqTag) or \
            isinstance(item, LogseqComposedTag) or \
            isinstance(item, LogseqSquareTag):

            self.tags.extend(item.target)

        elif isinstance(item, LogseqScheduled):

            self.scheduled = item.target

        elif isinstance(item, LogseqDeadline):

            self.deadline = item.target

        elif \
            isinstance(item, marko.inline.LineBreak) or \
            isinstance(item, marko.block.BlankLine) or \
            isinstance(item, LogseqLogBook) or \
            isinstance(item, LogseqEnd):

            pass


    # ----------------------------------
    #
    # Expand this block making copies of it for each logbook entry.
    #
    # ----------------------------------
    def get_logbook_copies(self) -> list[ClockBlock]:

        from .clockblock import ClockBlock

        tuples = []

        for logbook_entry in self.logbook:
            tuples.append(ClockBlock(logbook_entry, self))

        return tuples


    # ----------------------------------
    #
    # __repr__ method.
    #
    # ----------------------------------
    def __repr__(self) -> str:
        """Print representation of the block.

        Returns:
            str: representation of the block.
        """
        graph_title = "No graph defined"
        page_title = "No page defined"

        if self.page:
            page_title = self.page.title

            if self.page.graph:
                graph_title = self.page.graph.title

        return f"Block({graph_title}, {page_title}, {self.title})"
