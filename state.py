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
    last_active: float = field(default_factory=time.time)

    def decay(self, rate=0.05):
        """每次 tick 衰减一次，不活跃的项会自然淡出"""
        self.salience = max(0.0, self.salience - rate)
        return self.salience


@dataclass
class BrainState:
    clock: int = 0
    wakefulness: float = 1.0
    focus: list = field(default_factory=list)
    goal: str = ""
    drives: dict = field(default_factory=dict)
    neuromod: dict = field(default_factory=dict)