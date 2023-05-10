from typing import Any, Protocol
import datetime

# ----------------------------------
#
# Forward declarations.
#
# ----------------------------------
class Graph(Protocol):
    path: str
    id: str
    title: str
    pages_file_name: list[str]
    pages: list[Any]

class Page(Protocol):
    content: str
    path: str
    blocks: list[Any]
    graph: Graph
    title: str

class Block(Protocol):
    id: str
    page: Any

class Clock(Protocol):
    start: datetime.datetime
    end: datetime.datetime

class ClockBlock(Protocol):
    clock: Clock
    block: Block
