from pylogseq import Block, Page, Graph
import datetime

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
        b = Block()

        assert b.content is None
        assert b.page is None
        assert b.order_in_page is None
        assert b.tags == []
        assert b.highest_priority is None
        assert b.done is False
        assert b.later is False
        assert b.now is False
        assert b.priorities == []
        assert b.logbook == []
        assert b.allocated_time is None
        assert b.scheduled is None
        assert b.deadline is None
        assert b.elapsed_time is None
        assert b.time_left is None
        assert b.is_title_block is False
        assert b.title is None
        assert b.id == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

        # Optional content
        b = Block(content="- A block")

        assert b.content == "- A block"
        assert b.page is None
        assert b.order_in_page is None
        assert b.tags == []
        assert b.highest_priority is None
        assert b.done is False
        assert b.later is False
        assert b.now is False
        assert b.priorities == []
        assert b.logbook == []
        assert b.allocated_time is None
        assert b.scheduled is None
        assert b.deadline is None
        assert b.elapsed_time is None
        assert b.time_left is None
        assert b.is_title_block is False
        assert b.title == "A block"
        assert b.id == "3a0da5506508afed4d93490ffc31a99dd291335412b595589698e154274f6949"

        # Optional page
        p = Page()
        b = Block(page=p)

        assert b.content is None
        assert isinstance(b.page, Page)
        assert b.order_in_page is None
        assert b.tags == []
        assert b.highest_priority is None
        assert b.done is False
        assert b.later is False
        assert b.now is False
        assert b.priorities == []
        assert b.logbook == []
        assert b.allocated_time is None
        assert b.scheduled is None
        assert b.deadline is None
        assert b.elapsed_time is None
        assert b.time_left is None
        assert b.is_title_block is False
        assert b.title is None
        assert b.id == "dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91"

        # Optional order in page
        b = Block(order_in_page=0)

        assert b.content is None
        assert b.page is None
        assert b.order_in_page == 0
        assert b.tags == []
        assert b.highest_priority is None
        assert b.done is False
        assert b.later is False
        assert b.now is False
        assert b.priorities == []
        assert b.logbook == []
        assert b.allocated_time is None
        assert b.scheduled is None
        assert b.deadline is None
        assert b.elapsed_time is None
        assert b.time_left is None
        assert b.is_title_block is False
        assert b.title is None
        assert b.id == "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"


    # ----------------------------------
    #
    # Test mutating ID.
    #
    # ----------------------------------
    def test_mutating_id(self):

        # Bare constructor
        b = Block()

        # Store the current ID
        current_id = b.id

        assert b.id == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

        # Add a page without a graph, ID should mutate
        p = Page()
        b.page = p

        assert b.id != current_id

        assert b.id == "dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91"

        # Add a graph to the page, ID should mutate
        g = Graph()
        p.graph = g
        b.page = p




    # TEST A PARSER WITH - AND WITHOUT -


    #     assert block.content == blockExampleSanitized
    #     assert block.priorities == [ "A", "C" ]
    #     assert block.tags == [ 'A', 'A/B', 'A/B/C', 'A/B/D', 'Composed tags', 'T', 'T/10' ]
    #     assert block.highest_priority == "A"
    #     assert block.done == True

    # # ----------------------------------
    # #
    # # Check DEADLINE and SCHEDULED
    # #
    # # ----------------------------------
    # def test_scheduled_deadline(self):
    #     """Scheduled and deadline test.
    #     """
    #     block = Block("""- A #T/10
    #         SCHEDULED: <2021-01-01 Fri 10:00>
    #         DEADLINE: <2021-01-02 Fri>
    #         :LOGBOOK:
    #         CLOCK: [2021-01-01 Wed 12:00:00]--[2021-01-01 Wed 12:10:00] =>  00:10:00
    #         CLOCK: [2021-01-01 Wed 12:20:00]--[2021-01-01 Wed 12:30:00] =>  00:10:00
    #         :END:""")

    #     assert block.scheduled == datetime.datetime(2021, 1, 1, 10, 0)
    #     assert block.deadline == datetime.datetime(2021, 1, 2, 0, 0)
    #     assert block.elapsed_time == datetime.timedelta(minutes=20)
    #     assert block.time_left == datetime.timedelta(hours=9, minutes=40)
