"""This class takes a top block (the ones starting by "- " in text read from a
Logseq page and parses it into Markdown, analyzing everything.

Child blocks are not parsed separately, they are part of the parent block.

TODO: THIS CLASS NEEDS A REVIEW IN DOC AFTER DROPPING THE S AND T OLD TAGS
FOR TIME CONTROL AND IMPLEMENTING THE S/PROJECT/ALLOCATED/SPRINT TAGS.
"""

import re
import marko
import datetime
from datetime import timedelta as td
from typing import Any, Self, List

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
from pylogseq.mdlogseq.elements_parsers.process_multi_tags import process_multi_tags

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
        waiting (bool):
            TODO
        priorities (list[str]):
            Unique priorities found in the block.
        clocks (list[Clock]):
            List of LogBook entries found in the block, as Clock objects.
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
            If the SCRUM tag is invalid.
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

        self.waiting: bool = False
        """Flag to signal that the block is marked as waiting.
        """

        self.priorities: list[str] = []
        """Unique priorities found in the block.
        """

        self.clocks: list[Clock] = []
        """List of LogBook entries found in the block, as Clock objects.
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
    # Total clocked time for the block.
    #
    # ----------------------------------
    @property
    def total_clocked_time(self) -> td:
        """Returns the total clocked time for the block.

        Returns:
            td: Total clocked time.
        """

        total: td = td(0)

        for clock in self.clocks:
            total += clock.elapsed

        return total


    # ----------------------------------
    #
    # Returns remaining backlog time, backlog time in the SCB tag minus total
    # clocked time. If it is less than 0 a timedelta of 0 is returned.
    #
    # ----------------------------------
    @property
    def scrum_remaining_backlog_time(self) -> td:
        """Returns remaining backlog time, backlog time in the SCB tag minus
        total clocked time. If it is less than 0 a timedelta of 0 is returned.

        Returns:
            td: A timedelta with the remaining backlog time, None if there is no
                SCRUM backlog time.
        """

        if self.scrum_backlog_time is None: return None

        diff: td = self.scrum_backlog_time - self.total_clocked_time

        return diff if diff > td(0) else td(0)


    # ----------------------------------
    #
    # Returns remaining current time, the time in SCC tags minus total clocked
    # in the given sprint period, which is a Clock object. If it is less than
    # 0 a timedelta of 0 is returned.
    #
    # ----------------------------------
    def scrum_remaining_current_time(self, period: Clock) -> td:
        """Returns remaining current time, the time in SCC tags minus total
        time clocked in the given period (usually a sprint) as a Clock interval.
        It it is less than 0 a timedelta of 0 is returned.

        Args:
            period (Clock): The period to calculate the intersections, usually
                a sprint.

        Returns:
            td: The remaining current time in the period, None if there is no
                SCRUM current time.
        """

        if self.scrum_current_time is None: return None

        diff: td = self.scrum_current_time - self.total_intersection_time(period)

        return diff if diff > td(0) else td(0)


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
                Raises an exception if the SCRUM S tag does not adhere to the
                S/Project/allocated/sprint format.
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
                self.clocks.append(item.target)

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
                with the given clock interval. Returns an empty list if no
                collisions at all.
        """

        # Clock intersection
        clocks: list[Clock] = [ c.intersect(clock) for c in self.clocks ]

        # Purge Nones
        return [ c for c in clocks if c is not None ]


    # ----------------------------------
    #
    # Returns total time as a timedelta of clocks intersecting another one.
    #
    # ----------------------------------
    def total_intersection_time(self, clock: Clock) -> datetime.timedelta:
        """Returns the total time as a timedelta of the clocks of this block
        as they intersect with the given clock interval.

        Args:
            clock (Clock): The interval to test intersections with.

        Returns:
            datetime.timedelta: Total time of intersection.
        """

        total_time: td = td(0)

        # Iterate intersections and sum
        for inter in self.intersect_clock(clock):
            total_time += inter.elapsed

        return total_time


    # ----------------------------------
    #
    # Add a tag to the end of the title (first line).
    #
    # ----------------------------------
    def add_tag_to_title(self, tag: str) -> Self:
        """Adds a tag to the block's title, the first line. This is very
        useful to add a tag to a block in the index graph, for example to
        note the origin of the block.

        Args:
            tag (str): The tag to add.

        Returns:
            Self: The block itself.
        """

        # Split content line by line
        lines: list[str] = self.content.split("\n")

        # Add tag to the end of the first line
        lines[0] += f" #[[{tag}]]"

        # Join the lines
        self.title = lines[0]
        self.content = "\n".join(lines)

        # Update tags
        self.tags.extend(process_multi_tags(tag))

        self.tags = list(sorted(list(set(self.tags))))

        # Return this
        return self


    # ----------------------------------
    #
    # Removes a tag from title (first line).
    #
    # ----------------------------------
    def remove_tag_from_title(self, tag: str) -> Self:
        # TODO: USE THE CLASS DOCSTRING SNIPPET HERE TO DOCUMENT THE CLASS
        # TODO: USE THE AUTODOCSTRING EXTENSION (CTRL + SHIFT + 2) TO DOCUMENT METHODS

        # Split content line by line
        lines: list[str] = self.content.split("\n")

        # Add tag to the end of the first line
        lines[0] = lines[0].replace(f"#[[{tag}]]", "") \
                           .replace(f"#{tag}", "").strip()

        # Join the lines
        self.title = lines[0]
        self.content = "\n".join(lines)

        # Update tags
        for tag in process_multi_tags(tag):
            self.tags.remove(tag)

        self.tags = list(sorted(list(set(self.tags))))

        # Return this
        return self


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

        return f"Block({self.title})"
