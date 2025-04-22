from dataclasses import dataclass, field
from typing import Dict, List
from .monster import Monster

@dataclass
class Room:
    name: str
    description: str
    exits: Dict[str, str]
    monsters: List[Monster] = field(default_factory=list)
