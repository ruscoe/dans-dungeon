import sys
import json
from models import Details, LootItem, Monster, Player, Room, GameConfig

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

def print_commands():
    print("Available commands:")
    print("look  : Look around")
    print("north : Move North")
    print("south : Move South")
    print("east  : Move East")
    print("west  : Move West")
    print("fight : Fight a monster")
    print("quit  : Exit game")

def look(room: Room) -> str:
    description = f"Room: {room.name}\n"
    description += f"Description: {room.description}\n"
    description += "Exits: " + ", ".join(room.exits) + "\n"
    if room.monsters:
        description += "Monsters:\n"
        for monster in room.monsters:
            description += f"  - {monster.name} (Health: {monster.health}, Damage: {monster.damage})\n"
    return description

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

    player = Player(health=100, defense="", weapon="")

    current_room = config.rooms[0].name

    print(f"You are in the {current_room}")

    print_commands()

if __name__ == "__main__":
    main()
