# --------------------------------------
#
# Process errors in CLOCK
#
# --------------------------------------

# TODO: DOCUMENT

class ErrorClock(Exception):

  message: str = None

  def __init__(self, message: str):
    self.message = message
