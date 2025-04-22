from dataclasses import dataclass, field
from typing import Dict, List
from .chest import Chest
from .monster import Monster

@dataclass
class Room:
    name: str
    description: str
    exits: Dict[str, str]
    chests: List[Chest] = field(default_factory=list)
    monsters: List[Monster] = field(default_factory=list)
