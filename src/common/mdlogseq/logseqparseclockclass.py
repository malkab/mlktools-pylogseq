from .elements_parsers.logseqcomposedtagclass import LogseqComposedTag
from .elements_parsers.logseqtagclass import LogseqTag
from .elements_parsers.logseqclockclass import LogseqClock
from .elements_parsers.logseqsquaretagclass import LogseqSquareTag

class LogseqParseClock:
  elements = [ LogseqComposedTag, LogseqTag, LogseqClock, LogseqSquareTag ]
