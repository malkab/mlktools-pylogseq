"""This class takes a top block (the ones starting by "- " in text read from a
Logseq page and parses it into Markdown, analyzing everything.

Child blocks are not parsed separately, they are part of the parent block.

TODO: THIS CLASS HAS BEEN DOCUMENTED.
"""

import re
import marko
import datetime
from typing import Any
from pylogseq.parser import Parser
from pylogseq.clock import Clock
from pylogseq.mdlogseq.elements_parsers.logseqdoneclass import LogseqDone
from pylogseq.mdlogseq.elements_parsers.logseqpriorityclass import LogseqPriority
from pylogseq.mdlogseq.elements_parsers.logseqclockclass import LogseqClock
from pylogseq.mdlogseq.elements_parsers.logseqlaterclass import LogseqLater
from pylogseq.mdlogseq.elements_parsers.logseqnowclass import LogseqNow
from pylogseq.mdlogseq.elements_parsers import LogseqTag
from pylogseq.mdlogseq.elements_parsers import LogseqComposedTag
from pylogseq.mdlogseq.elements_parsers import LogseqSquareTag
from pylogseq.mdlogseq.elements_parsers.logseqlogbookclass import LogseqLogBook
from pylogseq.mdlogseq.elements_parsers.logseqendclass import LogseqEnd
from pylogseq.mdlogseq.elements_parsers.logseqscheduledclass import LogseqScheduled
from pylogseq.mdlogseq.elements_parsers.logseqdeadlineclass import LogseqDeadline

# ----------------------------------
#
# Block class.
#
# ----------------------------------
class Block():
    """A class to represent a top level block in a page. Subblocks are processed
    as part of this block but not parsed on separate ones. We are only
    interested in top level ones.

    Attributes:
        content (str):
            Sanitized content of the block, in plain str, suitable for moving.
        tags (list[str]):
            List of unique tags found in the block.
        highest_priority (str):
            The highest priority found in the block.
        done (bool):
            Is the block marked as done?
        later (bool):
            Is the block marked as later?
        now (bool):
            Is the block marked as now?
        priorities (list[str]):
            Unique priorities found in the block.
        logbook (list[Clock]):
            List of LogBook entries found in the block, as Clock objects.
        allocated_time (int):
            Time allocated in the SCRUM Backlog, in the T tag.
        current_time (int):
            Time allocated in the SCRUM Current, in the S tag.
        scheduled (datetime.datetime):
            A scheduled date for the block, in the SCHEDULED tag.
        deadline (datetime.datetime):
            A deadline date for the block, in the DEADLINE tag.
        title (str):
            The title of the block, the first line of the content.

    Raises:
        Exception:
            If the block content is empty.
        Exception:
            If the allocated time is invalid.
        Exception:
            If the current time is invalid.
    """

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def __init__(self, content: str=None):
        """Constructor.

        Args:
            content (str):
                The block's content in a plain str. This will be parsed by the
                Markdown parser.
        """

        self.content: str = content.strip("\n").strip() if content else None
        """Sanitized content of the block. Content for a block must start with '- '.
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

        self.current_time: int = None
        """The time in S tags.
        """

        self.scheduled: datetime.datetime = None
        """The scheduled date for the block.
        """

        self.deadline: datetime.datetime = None
        """The deadline date for the block.
        """

        self.title: str = content.split("\n")[0].strip("- ").strip() if content \
            else None
        """The title of the block, the first line of the content, without '-'.
        """


    # ----------------------------------
    #
    # Parse the block content.
    #
    # ----------------------------------
    def parse(self) -> None:
        """Parses the block's content by initiating the recursive parsing of
        anidated blocks.

        Raises:
            Exception:
                Raises an exception if the block's content is empty.
            Exception:
                Raises an exception if the allocated time in T tags cannot be
                processed.
            Exception:
                Raises an exception if the current time in S tags cannot be
                processed.
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
                time_tag = int(re.sub(r"\D", "", time_tag))
                self.allocated_time = datetime.timedelta(hours=time_tag)

            except:
                raise Exception("Invalid allocated time tag: " + time_tag)

        # Check if there is an allocated SCRUM current time tag S
        if "S" in self.tags:

            time_tag = list(filter(lambda x: x.startswith("S/"), self.tags))[0]

            try:
                time_tag = int(re.sub(r"\D", "", time_tag))
                self.current_time = datetime.timedelta(hours=time_tag)

            except:
                raise Exception("Invalid current time tag: " + time_tag)


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
            if item.target:
                self.logbook.append(item.target)

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
    # Clock block intersections.
    #
    # ----------------------------------
    def intersect_clock(self, clock: Clock) -> list[Clock]:
        """Returns a list of Clock objects that are the intersections of the
        clocks in this block with the given clock interval.

        Args:
            clock (Clock):
                The Clock interval to compute intersections with.

        Returns:
            list[Clock]:
                The list of intersections of Clock objects in the block
                with the given clock interval.
        """

        # Clock intersection
        clocks: list[Clock] = [ c.intersect(clock) for c in self.logbook ]

        # Purge Nones
        return [ c for c in clocks if c is not None ]


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
