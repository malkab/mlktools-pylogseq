import datetime

import marko
from pylogseq.pylogseq.mdlogseq.elements_parsers import (
    process_multi_tags,
    LogseqTag,
    LogseqComposedTag,
    LogseqSquareTag,
    LogseqPriority,
    LogseqLogBook,
    LogseqLater,
    LogseqEnd,
    LogseqDone,
)
import pytest
from pylogseq.pylogseq.mdlogseq.exceptions.errorclock import ErrorClock
from pylogseq.pylogseq.parser import Parser

parser = Parser()


# @pytest.mark.skip
class TestParser:
    # ----------------------------------
    #
    # Simple parser test.
    #
    # ----------------------------------
    def test_parser_simple(self):
        """Parses a simple Markdown list."""
        p = parser.parse(
            """
- A
- B
- C
        """
        )

        assert type(p.children[1]) is marko.block.List

    # ----------------------------------
    #
    # Clock test.
    #
    # ----------------------------------
    # @pytest.mark.skip
    def test_clock(self):
        """Parses Logseq clock structures:

        CLOCK: [2022-11-25 Fri 12:17:38]--[2022-11-25 Fri 12:19:27] =>  00:01:49
        """

        markdown = """- DONE #[[Gestión/Gestión general]] Something
        :LOGBOOK:
        CLOCK: [2022-11-25 Fri 08:57:12]--[2022-11-25 Fri 09:09:45] =>  00:12:33
        CLOCK: [2022-11-25 Fri 10:01:13]--[2022-11-25 Fri 10:01:17] =>  00:00:04
        CLOCK: [2022-11-25 Fri 10:01:18]--[2022-11-25 Fri 10:07:58] =>  00:06:40
        CLOCK: [2022-11-25 Fri 12:17:38]--[2022-11-25 Fri 12:19:27] =>  00:01:49
        CLOCK: [2022-11-25 Fri 14:49:56]--[2022-11-25 Fri 14:54:06] =>  00:04:10
        :END:"""

        parsed = parser.parse(markdown)

        assert isinstance(parsed, marko.block.Document) is True
        assert isinstance(parsed.children[0], marko.block.List) is True

        listItem = parsed.children[0].children[0]  # type: ignore

        assert isinstance(listItem, marko.block.ListItem) is True

    # @pytest.mark.skip
    def test_composed_tag(self):
        """Parses Logseq composed tags and return the full list of qualified
        tags. For example,

        [[Work/Composed A]] will return the list [ "Work", "Work/Composed A" ].
        """
        markdown = """- #[[Work/Composed A]] [[A/B/Composed B]]"""

        parsed = parser.parse(markdown)

        listItem = parsed.children[0].children[0].children[0]  # type: ignore

        assert type(listItem) is marko.block.Paragraph
        assert type(listItem.children[0]) is LogseqComposedTag
        assert type(listItem.children[1]) is marko.inline.RawText  # type: ignore
        assert type(listItem.children[2]) is LogseqSquareTag

        assert listItem.children[0].target == ["Work", "Work/Composed A"]
        assert listItem.children[2].target == ["A", "A/B", "A/B/Composed B"]

    # @pytest.mark.skip
    def test_done(self):
        """Detects the DONE keyword."""
        markdown = """- DONE #[[Gestión/Gestión general]] Something"""

        parsed = parser.parse(markdown)

        b = parsed.children[0].children[0].children[0].children[0]  # type: ignore

        assert type(b) is LogseqDone
        assert b.target == "DONE"

    # @pytest.mark.skip
    def test_end(self):
        """Detects the END keyword."""
        markdown = """- Something
        :LOGBOOK:
        CLOCK: [2022-11-25 Fri 08:57:12]--[2022-11-25 Fri 09:09:45] =>  00:12:33
        :END:"""

        parsed = parser.parse(markdown)

        b = parsed.children[0].children[0].children[0].children[4]  # type: ignore

        assert type(b) is LogseqEnd
        assert b.target == ":END:"

    # @pytest.mark.skip
    def test_later(self):
        """Detects the LATER keyword."""
        markdown = """- LATER Something
        :LOGBOOK:
        CLOCK: [2022-11-25 Fri 08:57:12]--[2022-11-25 Fri 09:09:45] =>  00:12:33
        :END:"""

        parsed = parser.parse(markdown)

        b = parsed.children[0].children[0].children[0].children[0]  # type: ignore

        assert type(b) is LogseqLater
        assert b.target == "LATER"

    # @pytest.mark.skip
    def test_logbook(self):
        """Detects the LOGBOOK keyword."""
        markdown = """- LATER Something
        :LOGBOOK:
        CLOCK: [2022-11-25 Fri 23:54:59]--[2022-11-26 Sat 00:05:01] =>  00:12:33
        :END:"""

        parsed = parser.parse(markdown)

        b = parsed.children[0].children[0].children[0].children[3]  # type: ignore

        assert type(b) is LogseqLogBook
        assert b.target == ":LOGBOOK:"

    # @pytest.mark.skip
    def test_priority(self):
        """Detects the priority ABC keyword."""
        markdown = ["- [#A] Something", "- [#B] Something", "- [#C] Something"]

        out = []

        for m in markdown:
            parsed = parser.parse(m)

            b = parsed.children[0].children[0].children[0].children[0]  # type: ignore

            assert type(b) is LogseqPriority
            out.append(b.target)

        assert out == ["A", "B", "C"]

    # @pytest.mark.skip
    def test_square_tag(self):
        """Detects the [[tag]]."""
        markdown = "- Something [[tag]]"

        parsed = parser.parse(markdown)

        b = parsed.children[0].children[0].children[0].children[1]  # type: ignore

        assert type(b) is LogseqSquareTag
        assert b.target == ["tag"]

    # @pytest.mark.skip
    def test_tag(self):
        """Detects #tag."""
        markdown = "- #A Something #B Something #C"

        parsed = parser.parse(markdown)

        b = parsed.children[0].children[0].children[0]  # type: ignore

        assert type(b) is marko.block.Paragraph

        assert type(b.children[0]) is LogseqTag
        assert b.children[0].target == ["A"]

        assert type(b.children[2]) is LogseqTag
        assert b.children[2].target == ["B"]

        assert type(b.children[4]) is LogseqTag
        assert b.children[4].target == ["C"]

    # @pytest.mark.skip
    def test_mixed_tags(self):
        """Detects a mix of tags of different types."""
        markdown = """
- #A #[[C tag]] #A/B/C [[A/BB/C]] #C
- #[[C tag]] #A/B/C [[X/Y]] #[[A/BB/C]]
- [[X/Y]] #A #[[A/B/C]] [[T/B]]
"""

        parsed = parser.parse(markdown)

        l0 = parsed.children[1].children[0].children[0]  # type: ignore
        l1 = parsed.children[1].children[1].children[0]  # type: ignore
        l2 = parsed.children[1].children[2].children[0]  # type: ignore

        assert type(l0) is marko.block.Paragraph
        assert type(l1) is marko.block.Paragraph
        assert type(l2) is marko.block.Paragraph

        # l0
        assert type(l0.children[0]) is LogseqTag
        assert l0.children[0].target == ["A"]

        assert type(l0.children[2]) is LogseqComposedTag
        assert l0.children[2].target == ["C tag"]

        assert type(l0.children[4]) is LogseqTag
        assert l0.children[4].target == ["A", "A/B", "A/B/C"]

        assert type(l0.children[6]) is LogseqSquareTag
        assert l0.children[6].target == ["A", "A/BB", "A/BB/C"]

        assert type(l0.children[8]) is LogseqTag
        assert l0.children[8].target == ["C"]

        # l1
        assert type(l1.children[0]) is LogseqComposedTag
        assert l1.children[0].target == ["C tag"]

        assert type(l1.children[2]) is LogseqTag
        assert l1.children[2].target == ["A", "A/B", "A/B/C"]

        assert type(l1.children[4]) is LogseqSquareTag
        assert l1.children[4].target == ["X", "X/Y"]

        assert type(l1.children[6]) is LogseqComposedTag
        assert l1.children[6].target == ["A", "A/BB", "A/BB/C"]

        # l2
        assert type(l2.children[0]) is LogseqSquareTag
        assert l2.children[0].target == ["X", "X/Y"]

        assert type(l2.children[2]) is LogseqTag
        assert l2.children[2].target == ["A"]

        assert type(l2.children[4]) is LogseqComposedTag
        assert l2.children[4].target == ["A", "A/B", "A/B/C"]

        assert type(l2.children[6]) is LogseqSquareTag
        assert l2.children[6].target == ["T", "T/B"]

    def test_error_clock_malformed(self):
        """Clock parsing malformed, returning empty clock set."""
        markdown = """- DONE #[[Gestión/Gestión general]] Something
        :LOGBOOK:
        CLOCK: [2022-11-25 Fri 08:57:12]- e3 -[2022-11-25 Fri 09:09:45] =>  00:12:33
        :END:"""

        parsed = parser.parse(markdown)

        assert parsed.children[0].children[0].children[0].children[6].target is None  # type: ignore

    def test_error_clock_starting_timestamp(self):
        """Error parsing the starting timestamp."""
        with pytest.raises(ErrorClock) as e:
            markdown = """- DONE #[[Gestión/Gestión general]] Something
                :LOGBOOK:
                CLOCK: [2022-11-25.3 Fri 08:57:12]--[2022-11-25 Fri 09:09:45] =>  00:12:33
                :END:"""

            parser.parse(markdown)

        assert (
            e.value.message
            == "CLOCK error: unparseable start timestamp 2022-11-25.3 08:57:12"
        )

    def test_error_clock_ending_timestamp(self):
        """Error parsing the ending timestamp."""
        with pytest.raises(ErrorClock) as e:
            markdown = """- DONE #[[Gestión/Gestión general]] Something
                :LOGBOOK:
                CLOCK: [2022-11-25 Fri 08:57:12]--[2022-11-25.6 Fri 09:09:45] =>  00:12:33
                :END:"""

            parser.parse(markdown)

        assert (
            e.value.message
            == "CLOCK error: unparseable ending timestamp 2022-11-25.6 09:09:45"
        )

    def test_error_clock_start_bigger(self):
        """Error in clocking: starting time bigger than ending time."""
        with pytest.raises(ErrorClock) as e:
            markdown = """- DONE #[[Gestión/Gestión general]] Something
                :LOGBOOK:
                CLOCK: [2022-11-26 Fri 09:57:12]--[2022-11-26 Sat 09:09:45] =>  00:12:33
                :END:"""

            parser.parse(markdown)

        assert (
            e.value.message
            == "CLOCK error: start time bigger than end time 2022-11-26 09:57:12 > 2022-11-26 09:09:45"
        )

    def test_scheduled_deadline(self):
        """Tests the parsing of an scheduled and deadline section."""
        markdown = """- Board Meeting
  SCHEDULED: <2023-08-02 Wed>
  DEADLINE: <2023-08-06 Wed 10:00>"""

        parsed = parser.parse(markdown)

        assert (
            parsed.children[0]
            .children[0]  # type: ignore
            .children[0]
            .children[1]  # type: ignore
            .target
            == datetime.datetime(2023, 8, 2, 0, 0, 0)
        )

        assert (
            parsed.children[0]
            .children[0]  # type: ignore
            .children[0]
            .children[2]  # type: ignore
            .target
            == datetime.datetime(2023, 8, 6, 10, 0, 0)
        )

    # ----------------------------------
    #
    # Tests the parser process_multi_tags method.
    #
    # ----------------------------------
    # @pytest.mark.skip
    def test_process_multi_tags(self):
        """Tests the parser process_multi_tags method."""

        assert process_multi_tags("A/B/C") == ["A", "A/B", "A/B/C"]
