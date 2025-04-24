from dataclasses import dataclass
from typing import List
from .details import Details
from .loot import LootItem
from .room import Room

@dataclass
class GameConfig:
    details: Details
    starting_weapon: LootItem
    starting_armor: LootItem
    loot: List[LootItem]
    rooms: List[Room]
