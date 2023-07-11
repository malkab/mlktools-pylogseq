from pylogseq import Block, Clock
import datetime
import pytest

blockExample = """





- DONE [#C] #A/B/C [[A/B/D]] #[[Composed tags]] Blocks title #T/10
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

blockExampleSanitized = """- DONE [#C] #A/B/C [[A/B/D]] #[[Composed tags]] Blocks title #T/10
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
        assert b.allocated_time is None
        assert b.scheduled is None
        assert b.deadline is None
        assert b.title is None
        assert b.total_elapsed_time == datetime.timedelta(0)
        assert b.remaining_time == None

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
        assert b.allocated_time is None
        assert b.scheduled is None
        assert b.deadline is None
        assert b.title == "A block"
        assert b.total_elapsed_time == datetime.timedelta(0)
        assert b.remaining_time == None

    # ----------------------------------
    #
    # Check DEADLINE and SCHEDULED
    #
    # ----------------------------------
    def test_scheduled_deadline(self):
        """Scheduled and deadline test.
        """
        block = Block(content="""- A #T/10
            SCHEDULED: <2021-01-01 Fri 10:00>
            DEADLINE: <2021-01-02 Fri>
            :LOGBOOK:
            CLOCK: [2021-01-01 Wed 12:00:00]--[2021-01-01 Wed 12:10:00] =>  00:10:00
            CLOCK: [2021-01-01 Wed 12:20:00]--[2021-01-01 Wed 12:30:00] =>  00:10:00
            :END:""")

        block.parse()

        assert block.scheduled == datetime.datetime(2021, 1, 1, 10, 0)
        assert block.deadline == datetime.datetime(2021, 1, 2, 0, 0)
        assert block.total_elapsed_time == datetime.timedelta(seconds=1200)
        assert block.remaining_time == datetime.timedelta(seconds=34800)


    # ----------------------------------
    #
    # Check title.
    #
    # ----------------------------------
    def test_title(self):

        block = Block(content="""- [#A] A block at page **test_2_page** in graph **test_2** #T/10.
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:00:02
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:00:02
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:00:02
            :END:""")

        block.parse()

        assert block.title == "[#A] A block at page **test_2_page** in graph **test_2** #T/10."
        assert block.highest_priority == "A"
        assert block.allocated_time == datetime.timedelta(hours=10)
        assert block.total_elapsed_time == datetime.timedelta(seconds=3000)
        assert block.remaining_time == datetime.timedelta(seconds=33000)


    # ----------------------------------
    #
    # Check time.
    #
    # ----------------------------------
    def test_time(self):

        block: Block = Block(content="""- [#A] A block at page **test_2_page** in graph **test_2** #T/2 #S/1
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            - [#B] aaa""")

        block.parse()

        assert block.title == "[#A] A block at page **test_2_page** in graph **test_2** #T/2 #S/1"
        assert block.tags == [ "S", "S/1", "T", "T/2" ]
        assert block.done is False
        assert block.later is False
        assert block.now is False
        assert block.priorities == [ "A", "B" ]
        assert block.highest_priority == "A"
        assert block.allocated_time == datetime.timedelta(hours=2)
        assert block.current_time == datetime.timedelta(hours=1)
        assert block.total_elapsed_time == datetime.timedelta(seconds=3000)
        assert block.remaining_time == datetime.timedelta(seconds=4200)


    # ----------------------------------
    #
    # Check clock intersections.
    #
    # ----------------------------------
    def test_clock_intersection(self):

        clock: Clock = Clock(datetime.datetime(2023,5,10,11,25), datetime.datetime(2023,5,10,13,15))

        block: Block = Block(content="""- [#A] A block at page **test_2_page** in graph **test_2** #T/2 #S/1
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            - [#B] aaa""")

        block.parse()

        assert block.intersect_clock(clock) == [
            Clock(datetime.datetime(2023, 5, 10, 11, 25), datetime.datetime(2023, 5, 10, 11, 30)),
            Clock(datetime.datetime(2023, 5, 10, 13, 0), datetime.datetime(2023, 5, 10, 13, 15))
        ]

        clock: Clock = Clock(datetime.datetime(2023, 2, 10, 11, 25), datetime.datetime(2023, 2, 10, 13, 15))

        block: Block = Block(content="""- [#A] A block at page **test_2_page** in graph **test_2** #T/2 #S/1
            :LOGBOOK:
            CLOCK: [2023-05-08 Thu 11:20:00]--[2023-05-08 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 11:20:00]--[2023-05-10 Thu 11:30:00] =>  00:10:00
            CLOCK: [2023-05-10 Thu 13:00:00]--[2023-05-10 Thu 13:30:00] =>  00:30:00
            :END:
            - [#B] aaa""")

        block.parse()

        assert block.intersect_clock(clock) == []
