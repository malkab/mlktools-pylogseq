from pylogseq import Block, Page, Graph
import datetime
from pytest import raises

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
        assert b.title is None

        with raises(Exception, match="Can't compute ID for Block since content is None"):
            b.id

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
        assert b.title == "A block"

        with raises(Exception, match="Can't compute ID for Block since order_in_page is None"):
            b.id

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
        assert b.title is None

        with raises(Exception, match="Can't compute ID for Block since content is None"):
            b.id

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
        assert b.title is None

        with raises(Exception, match="Can't compute ID for Block since content is None"):
            b.id

        # Full constructor


    # ----------------------------------
    #
    # Test mutating ID.
    #
    # ----------------------------------
    def test_mutating_id(self):

        # Bare constructor
        g = Graph(path="a_graph")
        p = Page(path="page/a_page.md", graph=g)
        b = Block(content="- A block", order_in_page=0, page=p)

        # Store the current ID
        current_id = b.id
        assert b.id == "30bd5a7dd28f64d3bbf8de9b6e9c03b5b8d8235a07a8080027128ac074ffdb65"

        # Add a page without a graph, ID should mutate
        p.path = "page/another_page.md"
        b.page = p

        assert b.id != current_id

        assert b.id == "4ec5cd50035d7a601785e442f59b802ce6bfcc5a648a54f41d3e67cb73a7a04d"


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
        assert block.elapsed_time == datetime.timedelta(minutes=20)
        assert block.time_left == datetime.timedelta(hours=9, minutes=40)
