from dataclasses import dataclass, field
import time

@dataclass
class Item:
    id: str
    content: str
    source: str = "external"
    salience: float = 0.0
    valence: float = 0.0
    ts: float = field(default_factory=time.time)

@dataclass
class BrainState:
    clock: int = 0
    wakefulness: float = 1.0
    focus: list = field(default_factory=list)
    goal: str = ""
    drives: dict = field(default_factory=dict)
    neuromod: dict = field(default_factory=dict)