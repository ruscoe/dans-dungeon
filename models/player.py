from dataclasses import dataclass
from .loot import LootItem

@dataclass
class Player:
    health: int
    gold: int
    armor: LootItem
    weapon: LootItem
    current_room: str = None
