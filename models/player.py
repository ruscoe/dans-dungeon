from dataclasses import dataclass

@dataclass
class Player:
    health: int
    armor: str
    weapon: str
    current_room: str = None
