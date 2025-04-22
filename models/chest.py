from dataclasses import dataclass

@dataclass
class Chest:
    name: str
    opened: bool = False
