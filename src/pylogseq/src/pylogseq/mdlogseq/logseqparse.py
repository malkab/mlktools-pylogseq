from .elements_parsers.logseqclockclass import LogseqClock
from .elements_parsers.logseqcomposedtagclass import LogseqComposedTag
from .elements_parsers.logseqendclass import LogseqEnd
from .elements_parsers.logseqlogbookclass import LogseqLogBook
from .elements_parsers.logseqsquaretagclass import LogseqSquareTag
from .elements_parsers.logseqtagclass import LogseqTag

class LogseqParse:
  elements = [ LogseqClock, LogseqLogBook, LogseqEnd, LogseqComposedTag,
    LogseqTag, LogseqSquareTag ]
