from dataclasses import dataclass
from .clock import Clock
from .block import Block

@dataclass
class ClockBlock:
    clock: Clock
    block: Block
