# from elements_parsers.logseqclockclass import LogseqClock
# from elements_parsers.logseqcomposedtagclass import LogseqComposedTag
# from elements_parsers.logseqendclass import LogseqEnd
# from elements_parsers.logseqlogbookclass import LogseqLogBook
# from elements_parsers.logseqsquaretagclass import LogseqSquareTag
# from elements_parsers.logseqtagclass import LogseqTag
# from elements_parsers.logseqdoneclass import LogseqDone
# from elements_parsers.logseqlaterclass import LogseqLater
# from elements_parsers.logseqpriorityclass import LogseqPriority

import elements_parsers

class LogseqParse:

    elements = [ elements_parsers.LogseqDone, elements_parsers.LogseqLater,
        elements_parsers.LogseqClock, elements_parsers.LogseqLogBook,
        elements_parsers.LogseqEnd, elements_parsers.LogseqComposedTag,
        elements_parsers.LogseqTag, elements_parsers.LogseqSquareTag,
        elements_parsers.LogseqPriority ]


# ee44
#223ee33e
