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
    def __init__(self, start_date: datetime.datetime, end_date: datetime.datetime):

        self.start_date: datetime.datetime = start_date
        self.end_date: datetime.datetime = end_date
        self.elapsed_time: datetime.timedelta = self.end_date - self.start_date
