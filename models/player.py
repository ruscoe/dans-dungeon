from dataclasses import dataclass
from .loot import LootItem

@dataclass
class Player:
    health: int
    armor: LootItem
    weapon: LootItem
    current_room: str = None
