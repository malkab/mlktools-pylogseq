from .logseqcomposedtagclass import LogseqComposedTag
from .logseqtagclass import LogseqTag
from .logseqclockclass import LogseqClock

class Logseq:
  # elements = [ LogseqComposedTag, LogseqTag ]
  elements = [ LogseqComposedTag, LogseqTag, LogseqClock ]
