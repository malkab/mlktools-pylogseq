from .logseqcomposedtagclass import LogseqComposedTag
from .logseqtagclass import LogseqTag
from .logseqclockclass import LogseqClock
from .logseqsquaretagclass import LogseqSquareTag

class Logseq:
  elements = [ LogseqComposedTag, LogseqTag, LogseqClock, LogseqSquareTag ]
