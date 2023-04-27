from .elements_parsers.logseqclockclass import LogseqClock
from .elements_parsers.logseqcomposedtagclass import LogseqComposedTag
from .elements_parsers.logseqendclass import LogseqEnd
from .elements_parsers.logseqlogbookclass import LogseqLogBook
from .elements_parsers.logseqsquaretagclass import LogseqSquareTag
from .elements_parsers.logseqtagclass import LogseqTag
from .elements_parsers.logseqdoneclass import LogseqDone
from .elements_parsers.logseqlaterclass import LogseqLater
from .elements_parsers.logseqpriorityclass import LogseqPriority
from .elements_parsers.logseqnowclass import LogseqNow
from .elements_parsers.logseqscheduledclass import LogseqScheduled
from .elements_parsers.logseqdeadlineclass import LogseqDeadline
from .elements_parsers.logseqpagetitleclass import LogseqPageTitle


class LogseqParse:

    elements = [ LogseqDone, LogseqLater, LogseqDeadline, LogseqScheduled,
        LogseqClock, LogseqLogBook, LogseqEnd, LogseqComposedTag, LogseqTag,
        LogseqSquareTag, LogseqPriority, LogseqNow, LogseqPageTitle ]
