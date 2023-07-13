from pylogseq import Block, Clock
import datetime
import pytest

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

        assert block.scheduled == datetime.datetime(2021, 1, 1, 10, 0)
        assert block.deadline == datetime.datetime(2021, 1, 2, 0, 0)


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
            Block(content="""- A block at page **test_2_page** in graph **test_2** #SC/Test/2 #S/1""")

        block.parse()

        assert block.title == "A block at page **test_2_page** in graph **test_2** #SC/Test/2 #S/1"
        assert block.tags == ['S', 'S/1', 'SC', 'SC/Test', 'SC/Test/2']
        assert block.done is False
        assert block.later is False
        assert block.now is False
        assert block.priorities == [ ]
        assert block.highest_priority is None
        assert block.scrum_project == "Test"
        assert block.scrum_backlog_time == datetime.timedelta(hours=2)
        assert block.scrum_current_time == datetime.timedelta(hours=1)

        # No current time assigned
        block: Block = Block(content="""- A block at page **test_2_page** in graph **test_2** #SC/Test/2""")

        block.parse()

        assert block.title == "A block at page **test_2_page** in graph **test_2** #SC/Test/2"
        assert block.tags == ['SC', 'SC/Test', 'SC/Test/2']
        assert block.done is False
        assert block.later is False
        assert block.now is False
        assert block.priorities == [ ]
        assert block.highest_priority is None
        assert block.scrum_project == "Test"
        assert block.scrum_backlog_time == datetime.timedelta(hours=2)
        assert block.scrum_current_time is None

        # Done SCRUM
        block: Block = Block(content="""- DONE A block at page **test_2_page** in graph **test_2** #SC/Test""")

        block.parse()

        assert block.title == "DONE A block at page **test_2_page** in graph **test_2** #SC/Test"
        assert block.tags == ['SC', 'SC/Test']
        assert block.done is True
        assert block.later is False
        assert block.now is False
        assert block.priorities == [ ]
        assert block.highest_priority is None
        assert block.scrum_project == "Test"
        assert block.scrum_backlog_time is None
        assert block.scrum_current_time is None

        # Current sprint time assigned without SC tag
        block: Block = Block(content="""- A block at page **test_2_page** in graph **test_2** #S/1""")

        with pytest.raises(Exception, match="SCRUM S current time tag found without a project."):
            block.parse()

        # Malformed SC tag
        block: Block = Block(
            content="- [#A] A block at page **test_2_page** in graph **test_2** #SC")

        with pytest.raises(Exception, match="Invalid SC SCRUM tag: SC"):
            block.parse()

        # SC tag without Backlog or Current time and not DONE
        block: Block = Block(
            content="- A block at page **test_2_page** in graph **test_2** #SC/Test")

        with pytest.raises(Exception, match="SCRUM SC tag found without Backlog time in a not DONE block."):
            block.parse()

        # DONE with Backlog time
        block: Block = Block(
            content="- DONE A block at page **test_2_page** in graph **test_2** #SC/Test/2")

        with pytest.raises(Exception, match="SCRUM with Backlog or Current time found in a DONE block."):
            block.parse()

        # DONE with Current time
        block: Block = Block(
            content="- DONE A block at page **test_2_page** in graph **test_2** #SC/Test/2 #S/2")

        with pytest.raises(Exception, match="SCRUM with Backlog or Current time found in a DONE block."):
            block.parse()


    # ----------------------------------
    #
    # Check clock intersections.
    #
    # ----------------------------------
    def test_clock_intersection(self):

        clock: Clock = Clock(datetime.datetime(2023,5,10,11,25), datetime.datetime(2023,5,10,13,15))

        block: Block = Block(content="""- A block at page **test_2_page** in graph **test_2**
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            """)

        block.parse()

        assert block.intersect_clock(clock) == [
            Clock(datetime.datetime(2023, 5, 10, 11, 25), datetime.datetime(2023, 5, 10, 11, 30)),
            Clock(datetime.datetime(2023, 5, 10, 13, 0), datetime.datetime(2023, 5, 10, 13, 15))
        ]

        clock: Clock = Clock(datetime.datetime(2023, 2, 10, 11, 25), datetime.datetime(2023, 2, 10, 13, 15))

        block: Block = Block(content="""- [#A] A block at page **test_2_page** in graph **test_2**
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            """)

        block.parse()

        assert block.intersect_clock(clock) == []
