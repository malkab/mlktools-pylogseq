from datetime import datetime as dt
from datetime import timedelta as td

import pytest
from pylogseq.pylogseq import Block, Clock

blockExample = """





- DONE [#C] #A/B/C [[A/B/D]] #[[Composed tags]] Blocks title
  collapsed:: true
  :LOGBOOK:
  CLOCK: [2023-01-11 Wed 12:39:45]--[2023-01-11 Wed 12:39:49] =>  00:00:04
  :END:
  pgh::whatver
  - [#A] Something .cat.
  - Nuño Domínguez es cofundador de Materia, la sección de Ciencia de EL PAÍS.
    Es licenciado en Periodismo por la Universidad Complutense de Madrid y
    Máster en Periodismo Científico por la Universidad de Boston (EE UU). Antes
    de EL PAÍS trabajó en medios como Público, El Mundo, La Voz de Galicia o la
    Agencia Efe.




"""

blockExampleSanitized = """- DONE [#C] #A/B/C [[A/B/D]] #[[Composed tags]] Blocks title
    collapsed:: true
    :LOGBOOK:
    CLOCK: [2023-01-11 Wed 12:39:45]--[2023-01-11 Wed 12:39:49] =>  00:00:04
    :END:
    pgh::whatver
    - [#A] Something .cat.
    - Nuño Domínguez es cofundador de Materia, la sección de Ciencia de EL PAÍS.
        Es licenciado en Periodismo por la Universidad Complutense de Madrid y
        Máster en Periodismo Científico por la Universidad de Boston (EE UU). Antes
        de EL PAÍS trabajó en medios como Público, El Mundo, La Voz de Galicia o la
        Agencia Efe."""


# @pytest.mark.skip
class TestBlock:
    # ----------------------------------
    #
    # Test constructor.
    #
    # ----------------------------------
    def test_block_constructor(self):
        """Test constructor and initial members status."""

        # Bare constructor
        b: Block = Block("")

        assert b.content == ""
        assert b.tags == []
        assert b.highest_priority is None
        assert b.done is False
        assert b.later is False
        assert b.now is False
        assert b.waiting is False
        assert b.priorities == []
        assert b.clocks == []
        assert b.scheduled is None
        assert b.deadline is None
        assert b.title == ""
        assert b.clean_title == ""
        assert b.repetitive is False
        assert b.repetitive_priority is False
        assert b.repetitive_period is None

        # Optional content
        b = Block(content="- A block")

        assert b.content == "- A block"
        assert b.tags == []
        assert b.highest_priority is None
        assert b.done is False
        assert b.later is False
        assert b.now is False
        assert b.waiting is False
        assert b.priorities == []
        assert b.clocks == []
        assert b.scheduled is None
        assert b.deadline is None
        assert b.title == "A block"
        assert b.clean_title == "A block"
        assert b.repetitive is False
        assert b.repetitive_priority is False
        assert b.repetitive_period is None

    # ----------------------------------
    #
    # Check DEADLINE and SCHEDULED
    #
    # ----------------------------------
    def test_scheduled_deadline(self):
        """Scheduled and deadline test."""
        block = Block(
            content="""- A
            SCHEDULED: <2021-01-01 Fri 10:00>
            DEADLINE: <2021-01-02 Fri>
            """
        )

        block.parse()

        assert block.scheduled == dt(2021, 1, 1, 10, 0)
        assert block.deadline == dt(2021, 1, 2, 0, 0)

    # ----------------------------------
    #
    # Check title.
    #
    # ----------------------------------
    def test_title(self):
        block = Block(
            content="""- [#A] A block at page **test_2_page** in graph **test_2** #T"""
        )

        block.parse()

        assert (
            block.title == "[#A] A block at page **test_2_page** in graph **test_2** #T"
        )
        assert block.clean_title == "A block at page test_2_page in graph test_2"

    # ----------------------------------
    #
    # Check SCRUM tag.
    #
    # ----------------------------------
    def test_scrum(self):
        # Full
        block: Block = Block(
            content="""- SCRUM TEST #P/Client/Project/SubactivityA #SCB/2 #SCC/1"""
        )

        block.parse()

        assert block.title == "SCRUM TEST #P/Client/Project/SubactivityA #SCB/2 #SCC/1"
        assert (
            block.clean_title == "SCRUM TEST P/Client/Project/SubactivityA SCB/2 SCC/1"
        )
        assert block.tags == [
            "P",
            "P/Client",
            "P/Client/Project",
            "P/Client/Project/SubactivityA",
            "SCB",
            "SCB/2",
            "SCC",
            "SCC/1",
        ]
        assert block.done is False
        assert block.later is False
        assert block.now is False
        assert block.priorities == []
        assert block.highest_priority is None

        # No current time assigned
        block: Block = Block(
            content="""- SCRUM TEST #P/Client/Project/SubactivityB #SCB/2"""
        )

        block.parse()

        assert block.title == "SCRUM TEST #P/Client/Project/SubactivityB #SCB/2"
        assert block.clean_title == "SCRUM TEST P/Client/Project/SubactivityB SCB/2"
        assert block.tags == [
            "P",
            "P/Client",
            "P/Client/Project",
            "P/Client/Project/SubactivityB",
            "SCB",
            "SCB/2",
        ]
        assert block.done is False
        assert block.later is False
        assert block.now is False
        assert block.priorities == []
        assert block.highest_priority is None

        # Done SCRUM
        block: Block = Block(content="""- DONE SCRUM TEST #P/Client""")

        block.parse()

        assert block.title == "DONE SCRUM TEST #P/Client"
        assert block.clean_title == "SCRUM TEST P/Client"
        assert block.tags == ["P", "P/Client"]
        assert block.done is True
        assert block.later is False
        assert block.now is False
        assert block.priorities == []
        assert block.highest_priority is None

    # ----------------------------------
    #
    # Check clock intersections.
    #
    # ----------------------------------
    def test_clock_intersection(self):
        clock: Clock = Clock(dt(2023, 5, 10, 11, 25), dt(2023, 5, 10, 13, 15))

        block: Block = Block(
            content="""- A block at page **test_2_page** in graph **test_2** #T
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            """
        )

        block.parse()

        assert block.intersect_clock(clock) == [
            Clock(dt(2023, 5, 10, 11, 25), dt(2023, 5, 10, 11, 30)),
            Clock(dt(2023, 5, 10, 13, 0), dt(2023, 5, 10, 13, 15)),
        ]

        clock: Clock = Clock(dt(2023, 2, 10, 11, 25), dt(2023, 2, 10, 13, 15))

        block: Block = Block(
            content="""- [#A] A block at page **test_2_page** in graph **test_2** #T
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            """
        )

        block.parse()

        assert block.intersect_clock(clock) == []

        # Test total intersection time
        clock: Clock = Clock(dt(2023, 5, 10, 11, 25), dt(2023, 5, 10, 13, 15))

        block: Block = Block(
            content="""- A block at page **test_2_page** in graph **test_2** #T
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            """
        )

        block.parse()

        assert block.total_intersection_time(clock) == td(minutes=20)

        # Total clocked time
        block: Block = Block(
            content="""- A block at page **test_2_page** in graph **test_2** #T
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            """
        )

        block.parse()

        assert block.total_clocked_time == td(minutes=50)

    # ----------------------
    #
    # Bad SCRUM time.
    #
    # ----------------------
    def test_bad_scrum_time(self):
        """Tests if a bad (non number) time for T/ tags has been given."""

        block: Block = Block("- Bad SCRUM time #T/XXX")

        # Check exception triggers
        with pytest.raises(Exception):
            block.parse()