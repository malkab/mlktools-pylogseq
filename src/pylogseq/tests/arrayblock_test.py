from pytest import raises
from pylogseq import Graph, ArrayBlock, Block, Clock
from datetime import datetime as dt

# ----------------------------------
#
# Tests for ArrayBlock class.
#
# ----------------------------------
class TestArrayBlock:
    """TODO
    """

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def test_constructor(self):
        """TODO
        """
        # Bad constructor
        with raises(Exception, match="Argument must be a list of blocks."):
            ArrayBlock(None)

        # Empty list
        blocks = ArrayBlock([])
        assert len(blocks) == 0

        # List of blocks
        blocks = ArrayBlock([ Block() ])
        assert len(blocks) == 1


    # ----------------------------------
    #
    # Array blocks.
    #
    # ----------------------------------
    def test_array_block(self):
        """TODO
        """
        graph_a = Graph(path="tests/assets/pylogseq_test_graph")
        graph_b = Graph(path="tests/assets/test_2")

        graph_a.get_pages()
        graph_a.parse()

        graph_b.get_pages()
        graph_b.parse()

        blocks = ArrayBlock(graph_a.get_all_blocks() + graph_b.get_all_blocks())

        assert len(blocks) == 11

        # # Scheduled
        # assert [ b.scheduled for b in blocks ] == [
        #         None,
        #         None,
        #         None,
        #         None,
        #         dt(2023, 4, 25, 0, 0),
        #         None,
        #         None,
        #         None,
        #         None
        #     ]

        # # Clocks
        # assert [ b.logbook for b in blocks ] == [
        #         [ Clock(dt(2023, 4, 27, 11, 33, 27), dt(2023, 4, 27, 11, 33, 29)) ],
        #         [],
        #         [],
        #         [],
        #         [
        #             Clock(dt(2023, 4, 27, 23, 0, 0), dt(2023, 4, 28, 1, 0, 0)),
        #             Clock(dt(2023, 4, 27, 20, 0, 0), dt(2023, 4, 27, 21, 0, 0))
        #         ],
        #         [],
        #         [ Clock(dt(2023, 4, 27, 11, 35, 22), dt(2023, 4, 27, 11, 35, 27)) ],
        #         [],
        #         []
        #     ]

        # # ClockBlock
        # assert [ (b.block.id, b.clock) for b in blocks.get_clock_blocks() ] == [
        #         ('8854c4054f688dfcd930745ed15dfa625f92d78a255b7aef0d253f5420abb949',
        #          Clock(dt(2023, 4, 27, 11, 33, 27), dt(2023, 4, 27, 11, 33, 29))),
        #         ('487b9c2c783b0afef8049f5b447a72a68a1c26f5a620c121f3e95c5f82c937eb',
        #          Clock(dt(2023, 4, 27, 23, 0, 0), dt(2023, 4, 28, 1, 0, 0))),
        #         ('487b9c2c783b0afef8049f5b447a72a68a1c26f5a620c121f3e95c5f82c937eb',
        #          Clock(dt(2023, 4, 27, 20, 0, 0), dt(2023, 4, 27, 21, 0, 0))),
        #         ('223907ab91b2060ee92cf7cfab16b7f25fb1000db912c1723c4d6f83999224f9',
        #          Clock(dt(2023, 4, 27, 11, 35, 22), dt(2023, 4, 27, 11, 35, 27)))
        #     ]

        # # Filtered
        # interval_filtered = blocks.get_clock_blocks(filter_interval=
        #                              Clock(dt(2023, 4, 27, 23, 10, 00), dt(2023, 4, 27, 23, 20, 00)))

        # assert [ (b.block.id, b.clock) for b in interval_filtered ] == [
        #     ('487b9c2c783b0afef8049f5b447a72a68a1c26f5a620c121f3e95c5f82c937eb',
        #      Clock(dt(2023, 4, 27, 23, 10, 0), dt(2023, 4, 27, 23, 20, 0)))
        # ]
