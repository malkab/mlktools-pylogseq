from datetime import datetime as dt
from datetime import timedelta as td
from pylogseq.forward_declarations import Clock

# TODO: DOCUMENT

# ----------------------------------
#
# Class to describe a clock section.
#
# ----------------------------------
class Clock:
    """Description.

    Attributes:
        attribute (type): description

    Raises:
        exception: description
    """

    def __init__(self, start: dt, end: dt):
        """Constructor.

        Args:
            start (datetime.datetime): Start date.

            end (datetime.datetime): End date.
        """
        self._start: dt = start
        self._end: dt = end
        self._elapsed: td = self._end - self._start


    # ----------------------------------
    #
    # Property start.
    # Start date.
    #
    # ----------------------------------
    @property
    def start(self) -> dt:
        return self._start

    @start.setter
    def page(self, start: dt) -> None:
        self._start = start
        self._elapsed = self._end - self._start


    # ----------------------------------
    #
    # Property end.
    # End date.
    #
    # ----------------------------------
    @property
    def end(self) -> dt:
        return self._end

    @start.setter
    def page(self, end: dt) -> None:
        self._end = end
        self._elapsed = self._end - self._start


    # ----------------------------------
    #
    # Property elapsed.
    # Elapsed time.
    #
    # ----------------------------------
    @property
    def elapsed(self) -> td:
        return self._elapsed


    # ----------------------------------
    #
    # Modify the clock member with the intersection with another Clock object.
    #
    # ----------------------------------
    def intersect(self, clock: Clock) -> Clock:
        """TODO

        Args:
            clock (Clock): _description_
        """
        start1, end1 = self.start, self.end
        start2, end2 = clock.start, clock.end

        # Find the intersection
        start_intersect = max(start1, start2)
        end_intersect = min(end1, end2)

        if start_intersect < end_intersect:
            return Clock(start_intersect, end_intersect)
        else:
            return None


    # ----------------------------------
    #
    # Built in methods.
    #
    # ----------------------------------
    def __repr__(self):
        return f"Clock({self.start}, {self.end})"

    def __eq__(self, other) -> bool:
        return type(self.start) == type(other.start) and \
                type(self.end) == type(other.end) and \
                self.start == other.start and \
                self.end == other.end
