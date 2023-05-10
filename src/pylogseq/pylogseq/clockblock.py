from pylogseq.clock import Clock
from pylogseq.block import Block
from pylogseq.forward_declarations import ClockBlock

# ----------------------------------
#
# Class ClockBlock.
#
# ----------------------------------
class ClockBlock():
    """Description.

    Attributes:
        attribute (type): description

    Raises:
        exception: description
    """

    # ----------------------------------
    #
    # Constructor.
    #
    # ----------------------------------
    def __init__(self, clock: Clock, block: Block):
        """Block comment
        """
        self.clock = clock
        self.block = block


    # ----------------------------------
    #
    # Modify the clock member with the intersection with another Clock object.
    #
    # ----------------------------------
    def intersect(self, clock: Clock) -> ClockBlock:
        """TODO

        Args:
            clock (Clock): _description_
        """
        start1, end1 = self.clock.start, self.clock.end
        start2, end2 = clock.start, clock.end

        # Find the intersection
        start_intersect = max(start1, start2)
        end_intersect = min(end1, end2)

        if start_intersect < end_intersect:
            # The intervals intersect
            self.clock = Clock(start_intersect, end_intersect)
        else:
            # The intervals do not intersect
            self.clock = None


    # ----------------------------------
    #
    # Built-in methods.
    #
    # ----------------------------------
    def __repr__(self):
        return f"ClockBlock({self.block}, {self.clock})"
