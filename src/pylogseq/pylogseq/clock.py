import datetime

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

    def __init__(self, start_time: datetime.datetime, end_time: datetime.datetime):
        """Constructor.

        Args:
            start_time (datetime.datetime): Start date.

            end_time (datetime.datetime): End date.
        """
        self.start_time: datetime.datetime = start_time
        self.end_time: datetime.datetime = end_time
        self.elapsed_time: datetime.timedelta = self.end_time - self.start_time


    # ----------------------------------
    #
    # Built in methods.
    #
    # ----------------------------------
    def __repr__(self):
        return f"Clock({self.start_time}, {self.end_time})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Clock):
            return self.start_time == other.start_time and self.end_time == other.end_time

        return NotImplemented
