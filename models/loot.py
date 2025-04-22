from dataclasses import dataclass
from typing import Optional

@dataclass
class LootItem:
    name: str
    type: str
    damage: Optional[int] = None
    defense: Optional[int] = None
