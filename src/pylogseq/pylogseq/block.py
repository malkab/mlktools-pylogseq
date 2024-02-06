"""This class takes a top block (the ones starting by "- " in text read from a
Logseq page and parses it into Markdown, analyzing everything.

Child blocks are not parsed separately, they are part of the parent block.

TODO: THIS CLASS NEEDS A REVIEW IN DOC AFTER DROPPING THE S AND T OLD TAGS
FOR TIME CONTROL AND IMPLEMENTING THE S/PROJECT/ALLOCATED/SPRINT TAGS.
"""

import datetime
import re
from datetime import timedelta as td
from typing import Any

import marko
import marko.inline as marko_inline

from pylogseq.pylogseq.clock import Clock
from pylogseq.pylogseq.mdlogseq.elements_parsers import (
    LogseqComposedTag,
    LogseqSquareTag,
    LogseqTag,
)
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqclockclass import LogseqClock
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqdeadlineclass import (
    LogseqDeadline,
)
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqdoneclass import LogseqDone
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqendclass import LogseqEnd
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqlaterclass import LogseqLater
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqlogbookclass import LogseqLogBook
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqnowclass import LogseqNow
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqpriorityclass import (
    LogseqPriority,
)
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqscheduledclass import (
    LogseqScheduled,
)
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqwaitingclass import LogseqWaiting
from pylogseq.pylogseq.parser import Parser
from pylogseq.pylogseq.scrum_status import SCRUM_STATUS

# TODO: revisar los imports y documentar


# ----------------------------------
#
# Block class.
#
# ----------------------------------
class Block:
    """A class to represent a top level block in a page. Subblocks are processed
    as part of this block but not parsed on separate ones. We are only
    interested in top level ones.

    TODO: AQUÍ HAN CAMBIADO MUCHAS COSAS, REVISAR, REVISAR TODAS LAS API DE LAS
    CLASES.

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

        self.title: str = content.split("\n")[0].strip().strip("- ").strip()
        """The title of the block, the first line of the content, without '-'.
        """

        self.scrum_status: SCRUM_STATUS = SCRUM_STATUS.NONE
        """SCRUM status, NONE by default. Will be set when parsing
        occurs.
        """

        self.scrum_time: int = 0
        """SCRUM time, by default 0."""

        self.repetitive: bool = False
        """Non-priority repetitive task."""

        self.repetitive_priority: bool = False
        """Priority repetitive task."""

        self.repetitive_period: int | None = None
        """Period of repetition."""

        self.repetitive_score: float | None = None
        """This is a synthetic score for repetitive tasks that represents its
        delayeness. It is the ratio between the time elapsed in days from the
        scheduled date and the number of days in its period. If equal to 1,
        it has reached its period, if bigger, it has passed its period, if lower
        than 0, it is still in its period."""

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

    # ----------------------
    #
    # A clean version of the title of the block, stripping many marks and tags.
    #
    # ----------------------
    @property
    def clean_title(self) -> str:
        """Cleans a block title from WAITING, LATER, [#ABC] and #T tags."""

        # Drop the #T/X tags
        t = re.sub(r"#T/\d+", "", self.title)

        # Drop common stuff
        t: str = (
            t.replace("WAITING", "")
            .replace("LATER", "")
            .replace("NOW", "")
            .replace("DONE", "")
            .replace("**", "")
            .replace("[#A]", "")
            .replace("[#B]", "")
            .replace("[#C]", "")
            .replace("#T", "")
            .replace("#", "")
        )

        # Drop [[ and ]]
        t = t.replace("[[", "").replace("]]", "")

        return t.strip()

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

        # Check for repetitive flag R/X plus period time for non-priority
        # repetitive tasks
        if "R" in self.tags or "RA" in self.tags:
            # Check there is a scheduled date
            if self.scheduled is None:
                raise Exception(
                    f"Repetitive task '{self.title}' has no scheduled date."
                )

            # By default, period to "1 week"
            self.repetitive_period = 1

            if "R" in self.tags:
                tag_to_look: str = "R/"
            else:
                tag_to_look: str = "RA/"

            # Look for the tag
            for t in self.tags:
                if t.startswith(tag_to_look):
                    try:
                        self.repetitive_period = int(t.split("/")[1])
                    except Exception:
                        raise Exception(
                            f"Invalid repetitive tag '{t}' in block {self.title}."
                        )

            # Repetitive flag
            if "R" in self.tags:
                self.repetitive = True
            else:
                self.repetitive_priority = True

            # Check if there is a scheduled date
            if self.scheduled is not None:
                # Calculate the repetitive score
                self.repetitive_score = (
                    (datetime.datetime.now() - self.scheduled).days
                ) / (int(self.repetitive_period) * 7)

        # Check for highest priority
        if len(self.priorities) > 0:
            self.highest_priority = self.priorities[0]

        # Check for SCRUM status. Repetitive tasks are not checked for SCRUM
        if self.repetitive is False and self.repetitive_priority is False:
            # First, check for LATER or NOW, which are DOING irrespective of the ABC
            if self.later is True or self.now is True:
                # If there is no T time tag, set to default 1 hour
                if self.scrum_time == 0:
                    self.scrum_time = 1

                self.scrum_status = SCRUM_STATUS.DOING

            # DONE, should not have T tag
            elif self.done is True:
                if self.scrum_time > 0:
                    self.scrum_time = 0
                self.scrum_status = SCRUM_STATUS.DONE

            # WAITING
            elif self.waiting is True:
                self.scrum_status = SCRUM_STATUS.WAITING
                if self.scrum_time == 0:
                    self.scrum_time = 1

            # Icebox, C
            elif self.highest_priority == "C":
                self.scrum_status = SCRUM_STATUS.ICEBOX

            # Backlog, B
            elif self.highest_priority == "B":
                # If there is no T time tag, set to default 1 hour
                if self.scrum_time == 0:
                    self.scrum_time = 1

                self.scrum_status = SCRUM_STATUS.BACKLOG

            # Current, priority, A
            elif self.highest_priority == "A":
                # If there is no T time tag, set to default 1 hour
                if self.scrum_time == 0:
                    self.scrum_time = 1

                self.scrum_status = SCRUM_STATUS.CURRENT

            # If LATER or NOW, it is DOING
            elif self.later is True or self.now is True:
                # If there is no T time tag, set to default 1 hour
                if self.scrum_time == 0:
                    self.scrum_time = 1

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

        elif isinstance(item, LogseqScheduled):
            self.scheduled = item.target

        elif isinstance(item, LogseqDeadline):
            self.deadline = item.target

        elif (
            isinstance(item, LogseqTag)
            or isinstance(item, LogseqComposedTag)
            or isinstance(item, LogseqSquareTag)
        ):
            self.tags.extend(item.target)

        elif (
            isinstance(item, marko_inline.LineBreak)
            or isinstance(item, marko.block.BlankLine)
            or isinstance(item, LogseqLogBook)
            or isinstance(item, LogseqEnd)
        ):
            pass

    # ----------------------------------
    #
    # Clock block intersections.
    #
    # ----------------------------------
    def intersect_clock(self, clock: Clock) -> list[Clock | None]:
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
        clocks: list[Clock | None] = [c.intersect(clock) for c in self.clocks]

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
    # __repr__ method.
    #
    # ----------------------------------
    def __repr__(self) -> str:
        """Print representation of the block.

        Returns:
            str: representation of the block.
        """

        return f"Block({self.title})"
