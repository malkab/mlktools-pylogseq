"""This class takes a top block (the ones starting by "- " in text read from a
Logseq page and parses it into Markdown, analyzing everything.

Child blocks are not parsed separately, they are part of the parent block.

TODO: THIS CLASS NEEDS A REVIEW IN DOC AFTER DROPPING THE S AND T OLD TAGS
FOR TIME CONTROL AND IMPLEMENTING THE S/PROJECT/ALLOCATED/SPRINT TAGS.
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

    How SCRUM Works

    A block can be given special tags to be used in SCRUM:

    - SC/project/X:         SCRUM Backlog time X for project.
    - SC/project/X + S/X:   SCRUM Sprint time X for project.
    - SC/project + DONE:    SCRUM DONE task for project.

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
        clocks (list[Clock]):
            List of LogBook entries found in the block, as Clock objects.
        scrum_project (str):
            The SCRUM project SC tags.
        scrum_backlog_time (int):
            The SCRUM Backlog time in SC/Project/X tag.
        scrum_current_time (int):
            The SCRUM sprint time in S/X time tags.
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

        self.priorities: list[str] = []
        """Unique priorities found in the block.
        """

        self.clocks: list[Clock] = []
        """List of LogBook entries found in the block, as Clock objects.
        """

        self.scrum_project: str = None
        """The tag that identifies the SCRUM project, if any. It is the second
        item in a SCRUM S/Project/allocated/sprint tag. Must be present.
        """

        self.scrum_backlog_time: datetime.timedelta = None
        """The allocated time for the block found in SCRUM tags. It is the third
        item in a SCRUM S/Project/allocated/sprint tag. Must be present.
        """

        self.scrum_current_time: datetime.timedelta = None
        """The sprint time for the block found in SCRUM tags. It is the fourth
        item in a SCRUM S/Project/allocated/sprint tag. Can be absent.
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

        # Check for SC SCRUM TAGS
        if "SC" in self.tags:

            # Try to parse the SCRUM tag
            try:
                time_tag = list(filter(lambda x: x.startswith("SC/"), self.tags))

                # A default value for tag to make the exception work at except
                tag = "SC"

                # Get the longest tag, which is the most specific
                tag = sorted(time_tag, key=len)[-1]

                # Use a regex to get the elements S/Project/allocated/sprint
                # and split them
                t = re.sub(r"SC/", "", tag)
                t = t.split("/")

                # Get components. The last one is optional.
                self.scrum_project = t[0]

                # Check if there is a backlog time
                self.scrum_backlog_time = datetime.timedelta(hours=int(t[1])) \
                    if len(t) == 2 else None

            except Exception as e:

                raise Exception("Invalid SC SCRUM tag: " + tag)

        # Check if there is a SCRUM tag S for current time
        if "S" in self.tags:

            # Try to parse the SCRUM tag
            try:
                time_tag = list(filter(lambda x: x.startswith("S/"), self.tags))

                # Get the longest tag, which is the most specific
                tag = sorted(time_tag, key=len)[-1]

                # Use a regex to get the elements S/Project/allocated/sprint
                # and split them
                t = re.sub(r"S/", "", tag)

                t = t.split("/")

                # Get components. The last one is optional.
                self.scrum_current_time = datetime.timedelta(hours=int(t[0]))

            except:
                raise Exception("Invalid S SCRUM tag: " + tag)

            # Raise exception if a S tag is found without a project
            if self.scrum_project is None:
                raise Exception("SCRUM S current time tag found without a project.")

        # Raise exception if SC tag is found without Backlog or current time in
        # a not DONE block
        if self.scrum_project is not None and \
            self.scrum_backlog_time is None and \
            self.scrum_current_time is None and \
            not self.done:
            raise Exception("SCRUM SC tag found without Backlog time in a not DONE block.")

        # Raise exception if there is Backlog or Current time while DONE
        if (self.scrum_backlog_time is not None or \
            self.scrum_current_time is not None) and \
            self.done:
            raise Exception("SCRUM with Backlog or Current time found in a DONE block.")

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
    # __repr__ method.
    #
    # ----------------------------------
    def __repr__(self) -> str:
        """Print representation of the block.

        Returns:
            str: representation of the block.
        """

        return f"Block({self.title})"
