"""This class takes a top block (the ones starting by "- " in text read from a
Logseq page and parses it into Markdown, analyzing everything.

Child blocks are not parsed separately, they are part of the parent block.

TODO: THIS CLASS NEEDS A REVIEW IN DOC AFTER DROPPING THE S AND T OLD TAGS
FOR TIME CONTROL AND IMPLEMENTING THE S/PROJECT/ALLOCATED/SPRINT TAGS.
"""

import datetime
from datetime import timedelta as td
from typing import Any, List, Self

import marko
import marko.inline as marko_inline

from pylogseq.clock import Clock
from pylogseq.mdlogseq.elements_parsers import (
    LogseqComposedTag,
    LogseqSquareTag,
    LogseqTag,
)
from pylogseq.mdlogseq.elements_parsers.logseqclockclass import LogseqClock
from pylogseq.mdlogseq.elements_parsers.logseqdeadlineclass import LogseqDeadline
from pylogseq.mdlogseq.elements_parsers.logseqdoneclass import LogseqDone
from pylogseq.mdlogseq.elements_parsers.logseqwaitingclass import LogseqWaiting
from pylogseq.mdlogseq.elements_parsers.logseqendclass import LogseqEnd
from pylogseq.mdlogseq.elements_parsers.logseqlaterclass import LogseqLater
from pylogseq.mdlogseq.elements_parsers.logseqlogbookclass import LogseqLogBook
from pylogseq.mdlogseq.elements_parsers.logseqnowclass import LogseqNow
from pylogseq.mdlogseq.elements_parsers.logseqpriorityclass import LogseqPriority
from pylogseq.mdlogseq.elements_parsers.logseqscheduledclass import LogseqScheduled
from pylogseq.mdlogseq.elements_parsers.process_multi_tags import process_multi_tags
from pylogseq.parser import Parser
from pylogseq.scrum_status import SCRUM_STATUS


# ----------------------------------
#
# Block class.
#
# ----------------------------------
class Block:
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
    def __init__(self, content: str):
        """Constructor.

        Args:
            content (str):
                The block's content in a plain str. This will be parsed by the
                Markdown parser.
        """

        self.content: str = content.strip("\n").strip()
        """Sanitized content of the block. Content for a block must start with '- '.
        """

        self.tags: list[str] = []
        """List of unique tags found in the block.
        """

        self.highest_priority: str | None = None
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

        self.scheduled: datetime.datetime | None = None
        """The scheduled date for the block.
        """

        self.deadline: datetime.datetime | None = None
        """The deadline date for the block.
        """

        self.title: str = content.split("\n")[0].strip("- ").strip()
        """The title of the block, the first line of the content, without '-'.
        """

        self.scrum_status: SCRUM_STATUS = SCRUM_STATUS.NONE
        """SCRUM status, NONE by default. Will be set when parsing
        occurs.
        """

        self.scrum_time: int = 0
        """SCRUM time, by default 0."""

        self.repetitive: bool = False
        """Repetitive task."""

        self.period: str | None = None
        """Period of repetition."""

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

        # Check for SCRUM status

        # First, check for LATER or NOW, which are DOING irrespective of the ABC
        if self.later is True or self.now is True:
            # Error if there is a SCRUM tag but no SCRUM time
            if self.scrum_time == 0 and "repetitiva" not in self.tags:
                raise Exception(
                    f"SCRUM time is 0 for block {self.title}, please set it to a positive integer."
                )

            self.scrum_status = SCRUM_STATUS.DOING

        # DONE, should not have T tag
        elif self.done is True:
            if self.scrum_time > 0:
                raise Exception(
                    f"SCRUM time is {self.scrum_time} for block {self.title}, please set it to 0."
                )

            self.scrum_status = SCRUM_STATUS.DONE

        # WAITING
        elif self.waiting is True:
            self.scrum_status = SCRUM_STATUS.WAITING

        # Icebox, C
        elif self.highest_priority == "C":
            self.scrum_status = SCRUM_STATUS.ICEBOX

        # Backlog, B
        elif self.highest_priority == "B":
            # Error if there is a SCRUM tag but no SCRUM time
            if self.scrum_time == 0 and self.repetitive is False:
                raise Exception(
                    f"SCRUM time is 0 for block {self.title}, please set it to a positive integer."
                )

            self.scrum_status = SCRUM_STATUS.BACKLOG

        # Current, priority, A
        elif self.highest_priority == "A":
            # Error if there is a SCRUM tag but no SCRUM time
            if self.scrum_time == 0 and self.repetitive is False:
                raise Exception(
                    f"SCRUM time is 0 for block {self.title}, please set it to a positive integer."
                )

            self.scrum_status = SCRUM_STATUS.CURRENT

            # If LATER, it is DOING
            if self.later is True or self.now is True:
                self.scrum_status = SCRUM_STATUS.DOING

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
        if (
            isinstance(item, marko.block.Document)
            or isinstance(item, marko.block.List)
            or isinstance(item, marko.block.ListItem)
            or isinstance(item, marko.block.Paragraph)
            or isinstance(item, marko.block.FencedCode)
            or isinstance(item, marko.block.Heading)
            or isinstance(item, marko_inline.StrongEmphasis)
        ):
            for child in item.children:
                self._process(child)

        elif isinstance(item, LogseqDone):
            self.done = True

        elif isinstance(item, marko_inline.RawText):
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

        elif isinstance(item, LogseqWaiting):
            self.waiting = True

        elif (
            isinstance(item, LogseqTag)
            or isinstance(item, LogseqComposedTag)
            or isinstance(item, LogseqSquareTag)
        ):
            self.tags.extend(item.target)

        elif isinstance(item, LogseqScheduled):
            self.scheduled = item.target

        elif isinstance(item, LogseqDeadline):
            self.deadline = item.target

        elif (
            isinstance(item, marko_inline.LineBreak)
            or isinstance(item, marko.block.BlankLine)
            or isinstance(item, LogseqLogBook)
            or isinstance(item, LogseqEnd)
        ):
            pass

        # Check if there is a SCRUM time tag
        if "T" in self.tags:
            # By default, SCRUM time is 1
            self.scrum_time = 1

            # Look for a T/X tag
            for t in self.tags:
                if t.startswith("T/"):
                    try:
                        self.scrum_time = int(t.split("/")[1])
                    except Exception:
                        raise Exception(
                            f"Invalid SCRUM time tag {t} in block {self.title}."
                        )

        # Check for repetitive flag R plus period time
        if "R" in self.tags:
            # By default, period to "1 week"
            self.period = "1 week"

            # Look for a R/X tag
            for t in self.tags:
                if t.startswith("R/"):
                    try:
                        self.period = t.split("/")[1]
                    except Exception:
                        raise Exception(
                            f"Invalid repetitive tag {t} in block {self.title}."
                        )

            # Repetitive flag
            self.repetitive = True

    # ----------------------------------
    #
    # Clock block intersections.
    #
    # ----------------------------------
    def intersect_clock(self, clock: Clock) -> List[Clock | None]:
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
        clocks: List[Clock | None] = [c.intersect(clock) for c in self.clocks]

        # Purge Nones
        return [c for c in clocks if c is not None]

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
            if inter is not None:
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
        lines[0] = lines[0].replace(f"#[[{tag}]]", "").replace(f"#{tag}", "").strip()

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
