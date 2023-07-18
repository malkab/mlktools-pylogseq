from pylogseq import Block, Clock
import pytest
from datetime import timedelta as td, datetime as dt

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

#@pytest.mark.skip
class TestBlock:

    # ----------------------------------
    #
    # Test constructor.
    #
    # ----------------------------------
    def test_block_constructor(self):
        """Test constructor and initial members status.
        """

        # Bare constructor
        b: Block = Block()

        assert b.content is None
        assert b.tags == []
        assert b.highest_priority is None
        assert b.done is False
        assert b.later is False
        assert b.now is False
        assert b.priorities == []
        assert b.clocks == []
        assert b.scrum_project is None
        assert b.scrum_backlog_time is None
        assert b.scrum_current_time is None
        assert b.scheduled is None
        assert b.deadline is None
        assert b.title is None

        # Optional content
        b = Block(content="- A block")

        assert b.content == "- A block"
        assert b.tags == []
        assert b.highest_priority is None
        assert b.done is False
        assert b.later is False
        assert b.now is False
        assert b.priorities == []
        assert b.clocks == []
        assert b.scrum_project is None
        assert b.scrum_backlog_time is None
        assert b.scrum_current_time is None
        assert b.scheduled is None
        assert b.deadline is None
        assert b.title == "A block"

    # ----------------------------------
    #
    # Check DEADLINE and SCHEDULED
    #
    # ----------------------------------
    def test_scheduled_deadline(self):
        """Scheduled and deadline test.
        """
        block = Block(content="""- A
            SCHEDULED: <2021-01-01 Fri 10:00>
            DEADLINE: <2021-01-02 Fri>
            """)

        block.parse()

        assert block.scheduled == dt(2021, 1, 1, 10, 0)
        assert block.deadline == dt(2021, 1, 2, 0, 0)


    # ----------------------------------
    #
    # Check title.
    #
    # ----------------------------------
    def test_title(self):

        block = Block(content="""- [#A] A block at page **test_2_page** in graph **test_2**""")

        block.parse()

        assert block.title == "[#A] A block at page **test_2_page** in graph **test_2**"
        assert block.highest_priority == "A"
        assert block.scrum_project == None
        assert block.scrum_backlog_time == None


    # ----------------------------------
    #
    # Check SCRUM tag.
    #
    # ----------------------------------
    def test_scrum(self):

        # Full
        block: Block = \
            Block(content="""- SCRUM TEST #P/Client/Project/SubactivityA #SCB/2 #SCC/1""")

        block.parse()

        assert block.title == "SCRUM TEST #P/Client/Project/SubactivityA #SCB/2 #SCC/1"
        assert block.tags == ['P', 'P/Client', 'P/Client/Project', 'P/Client/Project/SubactivityA', 'SCB', 'SCB/2', 'SCC', 'SCC/1']
        assert block.done is False
        assert block.later is False
        assert block.now is False
        assert block.priorities == [ ]
        assert block.highest_priority is None
        assert block.scrum_project == "Client/Project"
        assert block.scrum_backlog_time == td(hours=2)
        assert block.scrum_current_time == td(hours=1)
        assert block.scrum_remaining_backlog_time == td(hours=2)
        assert block.scrum_remaining_current_time(
            Clock(dt(2023, 10, 10, 10, 00), dt(2023, 10, 11, 10, 00))) == td(hours=1)

        # No current time assigned
        block: Block = Block(content="""- SCRUM TEST #P/Client/Project/SubactivityB #SCB/2""")

        block.parse()

        assert block.title == "SCRUM TEST #P/Client/Project/SubactivityB #SCB/2"
        assert block.tags == ['P', 'P/Client', 'P/Client/Project', 'P/Client/Project/SubactivityB', 'SCB', 'SCB/2']
        assert block.done is False
        assert block.later is False
        assert block.now is False
        assert block.priorities == [ ]
        assert block.highest_priority is None
        assert block.scrum_project == "Client/Project"
        assert block.scrum_backlog_time == td(hours=2)
        assert block.scrum_current_time is None

        # Done SCRUM
        block: Block = Block(content="""- DONE SCRUM TEST #P/Client""")

        block.parse()

        assert block.title == "DONE SCRUM TEST #P/Client"
        assert block.tags == ['P', 'P/Client']
        assert block.done is True
        assert block.later is False
        assert block.now is False
        assert block.priorities == [ ]
        assert block.highest_priority is None
        assert block.scrum_project == "Client"
        assert block.scrum_backlog_time is None
        assert block.scrum_current_time is None

        # Incorrect project tag
        block: Block = Block(content="""- SCRUM TEST #P""")

        with pytest.raises(Exception, match="Invalid Project tag: SCRUM TEST #P"):
            block.parse()

        # Current sprint time assigned with SCC without SCB tag
        block: Block = Block(content="""- SCRUM TEST #SCC/1""")

        with pytest.raises(Exception, match="SCRUM SCC tag found without SCB tag: SCRUM TEST #SCC/1"):
            block.parse()

        # Backlog time assigned without project
        # Not needed to raise with SCC since SCC cannot exists without SCB
        # and this exception triggers first.
        block: Block = Block(
            content="- SCRUM TEST #SCB/1")

        with pytest.raises(Exception, match="SCRUM SCB assigned without P tag: SCRUM TEST #SCB/1"):
            block.parse()

        # Time SCB assigned to DONE
        # Not needed to raise with SCC since SCC cannot exists without SCB
        # and this exception triggers first.
        block: Block = Block(content="- DONE SCRUM TEST #P/Client/Project #SCB/1")

        with pytest.raises(Exception, match="SCRUM tags found in DONE block: DONE SCRUM TEST #P/Client/Project #SCB/1"):
            block.parse()


    # ----------------------------------
    #
    # Check clock intersections.
    #
    # ----------------------------------
    def test_clock_intersection(self):

        clock: Clock = Clock(dt(2023,5,10,11,25), dt(2023,5,10,13,15))

        block: Block = Block(content="""- A block at page **test_2_page** in graph **test_2**
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            """)

        block.parse()

        assert block.intersect_clock(clock) == [
            Clock(dt(2023, 5, 10, 11, 25), dt(2023, 5, 10, 11, 30)),
            Clock(dt(2023, 5, 10, 13, 0), dt(2023, 5, 10, 13, 15))
        ]

        clock: Clock = Clock(dt(2023, 2, 10, 11, 25), dt(2023, 2, 10, 13, 15))

        block: Block = Block(content="""- [#A] A block at page **test_2_page** in graph **test_2**
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            """)

        block.parse()

        assert block.intersect_clock(clock) == []

        # Test total intersection time
        clock: Clock = Clock(dt(2023,5,10,11,25), dt(2023,5,10,13,15))

        block: Block = Block(content="""- A block at page **test_2_page** in graph **test_2**
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            """)

        block.parse()

        assert block.total_intersection_time(clock) == td(minutes=20)

        # Total clocked time
        block: Block = Block(content="""- A block at page **test_2_page** in graph **test_2**
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            """)

        block.parse()

        assert block.total_clocked_time == td(minutes=50)
