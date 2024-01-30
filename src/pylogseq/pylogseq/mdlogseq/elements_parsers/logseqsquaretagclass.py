from marko import inline
from .process_multi_tags import process_multi_tags

# TODO: DOCUMENT


class LogseqSquareTag(inline.InlineElement):
    pattern = r"\[\[(\b.+?\b)\]\]"
    parse_children = True
    priority = 6

    def __init__(self, match):
        self.target = process_multi_tags(match.group(1))
