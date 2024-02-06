from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqclockclass import LogseqClock
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqcomposedtagclass import (
    LogseqComposedTag,
)
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
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqsquaretagclass import (
    LogseqSquareTag,
)
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqtagclass import LogseqTag
from pylogseq.pylogseq.mdlogseq.elements_parsers.logseqwaitingclass import LogseqWaiting


class LogseqParse:
    elements = [
        LogseqNow,
        LogseqWaiting,
        LogseqDone,
        LogseqLater,
        LogseqDeadline,
        LogseqScheduled,
        LogseqClock,
        LogseqLogBook,
        LogseqEnd,
        LogseqComposedTag,
        LogseqTag,
        LogseqSquareTag,
        LogseqPriority,
    ]

    parser_mixins = []

    renderer_mixins = []
