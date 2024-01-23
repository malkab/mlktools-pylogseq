from enum import Enum


class SCRUM_STATUS(Enum):
    """Enumeration for possible SCRUM status.

    Args:
        Enum (_type_): Possible SCRUM status.
    """

    NONE = -1  # No SCRUM status
    ICEBOX = 0  # [#C] Icebox
    BACKLOG = 1  # [#B] Backlog #T/3 (1 por defecto)
    CURRENT = 2  # [#A] Current #T/3
    DOING = 3  # LATER [#A] Doing #T/8
    WAITING = 4  # WAITING [#A] Waiting #T/8
    DONE = 5  # DONE Done
