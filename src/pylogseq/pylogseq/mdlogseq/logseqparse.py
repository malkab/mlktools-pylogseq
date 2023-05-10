from pylogseq.mdlogseq.elements_parsers.logseqclockclass import LogseqClock
from pylogseq.mdlogseq.elements_parsers.logseqcomposedtagclass import LogseqComposedTag
from pylogseq.mdlogseq.elements_parsers.logseqendclass import LogseqEnd
from pylogseq.mdlogseq.elements_parsers.logseqlogbookclass import LogseqLogBook
from pylogseq.mdlogseq.elements_parsers.logseqsquaretagclass import LogseqSquareTag
from pylogseq.mdlogseq.elements_parsers.logseqtagclass import LogseqTag
from pylogseq.mdlogseq.elements_parsers.logseqdoneclass import LogseqDone
from pylogseq.mdlogseq.elements_parsers.logseqlaterclass import LogseqLater
from pylogseq.mdlogseq.elements_parsers.logseqpriorityclass import LogseqPriority
from pylogseq.mdlogseq.elements_parsers.logseqnowclass import LogseqNow
from pylogseq.mdlogseq.elements_parsers.logseqscheduledclass import LogseqScheduled
from pylogseq.mdlogseq.elements_parsers.logseqdeadlineclass import LogseqDeadline


class LogseqParse:

    elements = [ LogseqDone, LogseqLater, LogseqDeadline, LogseqScheduled,
        LogseqClock, LogseqLogBook, LogseqEnd, LogseqComposedTag, LogseqTag,
        LogseqSquareTag, LogseqPriority, LogseqNow ]
