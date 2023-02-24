from pylogseq import Block, Parser

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

excluded_words = [ "antes", "como", "de", "el", "en", "es", "la", "o", "por",
  "y", "collapsed::", "true" ]

class TestBlock:

    def test_constructor(self):
        """Test constructor and initial members status.
        """
        block = Block(blockExample, excluded_words)

        assert block.content == blockExampleSanitized
        assert block.content_hash == '67641214929fb5c1bc0d7d35b5e55459f25cc669b209b1f096e2497f6e92d622'
        assert block.priorities == [ "A", "C" ]
        assert block.tags == [ 'A', 'A/B', 'A/B/C', 'A/B/D', 'Composed tags' ]
        assert block.highest_priority == "A"
        assert block.done == True
        assert block.words == [ 'agencia', 'blocks', 'boston', 'cat',
          'ciencia', 'científico', 'cofundador', 'complutense',
          'domínguez', 'ee', 'efe', 'galicia',
          'licenciado', 'madrid', 'materia', 'medios', 'mundo', 'máster',
          'nuño', 'país', 'periodismo', 'pgh::whatver', 'público',
          'sección', 'something', 'title', 'trabajó', 'universidad', 'uu',
          'voz' ]
