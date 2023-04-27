from typing import Any, Protocol

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


class ClockBlock(Protocol):
    clock: Any
    block: Any
