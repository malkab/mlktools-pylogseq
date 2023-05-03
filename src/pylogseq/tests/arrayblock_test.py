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
        graph_a = Graph(path="pylogseq/tests/assets/pylogseq_test_graph")
        graph_b = Graph(path="pylogseq/tests/assets/test_2")

        graph_a.get_pages()
        graph_a.parse()

        graph_b.get_pages()
        graph_b.parse()

        blocks = ArrayBlock(graph_a.get_all_blocks() + graph_b.get_all_blocks())

        assert len(blocks) == 9

        # Scheduled
        assert [ b.scheduled for b in blocks ] == [
                None,
                None,
                None,
                None,
                dt(2023, 4, 25, 0, 0),
                None,
                None,
                None,
                None
            ]

        assert [ Clock(dt(2023, 4, 27, 11, 33, 27), dt(2023, 4, 27, 11, 33, 29)) ] == [Clock(dt(2023, 4, 27, 11, 33, 27), dt(2023, 4, 27, 11, 33, 29))]

        assert dt(2023, 4, 27, 11, 33, 27) == dt(2023, 4, 27, 11, 33, 27)

        print("D: kkkk", type(blocks[0].logbook)) #[ b.logbook for b in blocks ][0])

        # Clocks
        assert [ b.logbook for b in blocks ][0][0].start_time == \
                Clock(dt(2023, 4, 27, 11, 33, 27), dt(2023, 4, 27, 11, 33, 29)).start_time
                # [],
                # [],
                # [],
                # [
                #     Clock(dt(2023, 4, 27, 23, 0, 0), dt(2023, 4, 27, 23, 59, 59)),
                #     Clock(dt(2023, 4, 28, 0, 0, 0), dt(2023, 4, 28, 1, 0, 0)),
                #     Clock(dt(2023, 4, 27, 20, 0, 0), dt(2023, 4, 27, 21, 0, 0))
                # ],
                # [],
                # [ Clock(dt(2023, 4, 27, 11, 35, 22), dt(2023, 4, 27, 11, 35, 27)) ],
                # [],
                # []
            # ]
