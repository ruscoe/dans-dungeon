from dataclasses import dataclass

@dataclass
class Player:
    health: int
    defense: str
    weapon: str
    current_room: str = None
