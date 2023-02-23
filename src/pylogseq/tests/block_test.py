from pylogseq import Block, Parser






blockExample = """





- DONE [#C] #A [[B]] Blocks title
  :LOGBOOK:
  CLOCK: [2023-01-11 Wed 12:39:45]--[2023-01-11 Wed 12:39:49] =>  00:00:04
  :END:
  pgh::whatver
  - [#A] Something




"""

blockExampleSanitized = """- DONE [#C] #A [[B]] Blocks title
  :LOGBOOK:
  CLOCK: [2023-01-11 Wed 12:39:45]--[2023-01-11 Wed 12:39:49] =>  00:00:04
  :END:
  pgh::whatver
  - [#A] Something"""

block = Block(blockExample)


class TestBlock:

    def test_constructor(self):
        """Test constructor and initial members status.
        """
        assert block.content == blockExampleSanitized
        assert block.content_hash == 'f770164d9fe40d6b0133a7de5d584abc39410b234c8f6b80f82ce0be96eab654'
        assert block.hash == None
        assert block.tags == []
        assert block.highest_priority == None
