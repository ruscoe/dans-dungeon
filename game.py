import sys
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Details:
    name: str
    description: str
    version: str

@dataclass
class LootItem:
    name: str
    type: str
    damage: Optional[int] = None
    defense: Optional[int] = None

@dataclass
class Monster:
    name: str
    health: int
    damage: int

@dataclass
class Room:
    name: str
    description: str
    exits: Dict[str, str]
    monsters: List[Monster] = field(default_factory=list)

@dataclass
class GameConfig:
    details: Details
    loot: List[LootItem]
    rooms: List[Room]

def parse_game_config(data: dict) -> GameConfig:
    details = Details(**data['details'])

    loot = [LootItem(**item) for item in data.get('loot', [])]

    rooms = []
    for room in data.get('rooms', []):
        monsters = [Monster(**m) for m in room.get('monsters', [])]
        room_obj = Room(
            name=room['name'],
            description=room['description'],
            exits=room['exits'],
            monsters=monsters
        )
        rooms.append(room_obj)

    return GameConfig(details=details, loot=loot, rooms=rooms)

def main():
    if len(sys.argv) != 2:
        print("Usage: python game.py <path_to_game_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        sys.exit(1)

    config = parse_game_config(data)

    print("\nGame loaded!\n")
    print(f"Name        : {config.details.name}")
    print(f"Description : {config.details.description}")
    print(f"Version     : {config.details.version}\n")

if __name__ == "__main__":
    main()
