from pylogseq.page import Page

# TODO: DOCUMENT


class PageParserError(Exception):
    def __init__(
        self,
        message: str,
        original_exception: Exception,
        page: Page,
        block_content: str,
    ):
        self.message = message
        self.original_exception = original_exception
        self.page = page
        self.block_content = block_content
