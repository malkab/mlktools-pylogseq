from .logseqlogbookclass import LogseqLogBook
from .logseqendclass import LogseqEnd
from .logseqclockclass import LogseqClock

class LogseqParseLog:
  elements = [ LogseqClock, LogseqLogBook, LogseqEnd ]
