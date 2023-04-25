from pylogseq import Block
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

    def test_constructor(self):
        """Test constructor and initial members status.
        """
        block = Block(blockExample)

        assert block.content == blockExampleSanitized
        assert block.priorities == [ "A", "C" ]
        assert block.tags == [ 'A', 'A/B', 'A/B/C', 'A/B/D', 'Composed tags', 'T', 'T/10' ]
        assert block.highest_priority == "A"
        assert block.done == True

    # ----------------------------------
    #
    # Check DEADLINE and SCHEDULED
    #
    # ----------------------------------
    def test_scheduled_deadline(self):
        """Scheduled and deadline test.
        """
        block = Block("""- A #T/10
            SCHEDULED: <2021-01-01 Fri 10:00>
            DEADLINE: <2021-01-02 Fri>
            :LOGBOOK:
            CLOCK: [2021-01-01 Wed 12:00:00]--[2021-01-01 Wed 12:10:00] =>  00:10:00
            CLOCK: [2021-01-01 Wed 12:20:00]--[2021-01-01 Wed 12:30:00] =>  00:10:00
            :END:""")

        assert block.scheduled == datetime.datetime(2021, 1, 1, 10, 0)
        assert block.deadline == datetime.datetime(2021, 1, 2, 0, 0)
        assert block.elapsed_time == datetime.timedelta(minutes=20)
        assert block.time_left == datetime.timedelta(hours=9, minutes=40)
