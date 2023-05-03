from .block import Block

# ----------------------------------
#
# A set of Blocks with utility methods for filtering and such.
#
# Often obtained from a set of Graph's get_all_blocks after Graph's
# parse_iter() method.
#
# ----------------------------------
class ArrayBlock:
    """TODO
    """

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def __init__(self, blocks: list[Block]):
        """TODO

        Args:
            blocks (list[Block], optional): The set of Block objects. Defaults to None.
        """
        if blocks is None:
            raise Exception("Argument must be a list of blocks.")

        self._blocks = blocks

        # Index for the iterable
        self._index = -1


    # ----------------------------------
    #
    # Iterable functions.
    #
    # ----------------------------------
    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1

        if self._index < len(self._blocks):
            return self._blocks[self._index]
        else:
            self._index = -1
            raise StopIteration

    def __len__(self):
        return len(self._blocks)

    def __getitem__(self, index):
        return self._blocks[index]
