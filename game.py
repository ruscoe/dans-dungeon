"""
Dan's Dungeon

A JSON-based game engine for a text-based dungeon crawlers.

Usage:
    python game.py <path_to_game_json_file>
"""

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
    print("look                           : Look around")
    print("go north / south / east / west : Move in a direction")
    print("fight                          : Fight a monster")
    print("quit                           : Exit game")

def look(room: Room):
    print(f"\n{room.description}")
    print("Exits:")
    for direction, destination in room.exits.items():
        print(f"  {direction.title()}: {destination}")
        if room.monsters:
            print("Monsters:")
            for monster in room.monsters:
                print(f"{monster.name} (HP: {monster.health}, DMG: {monster.damage})")

def move(player: Player, room: Room, direction: str):
    if direction in room.exits:
        destination = room.exits[direction]
        player.current_room = destination
        print(f"You go {direction} to {destination}.")
    else:
        print("You can't go that way.")

def game_loop(config: GameConfig, player: Player):
    rooms_by_name = {room.name: room for room in config.rooms}

    while True:
        current_room = rooms_by_name.get(player.current_room)
        print(f"\nYou are in: {current_room.name}")
        command = input("> ").strip().lower()

        if command == "quit":
            print("Goodbye!")
            break

        elif command == "look":
            look(current_room)

        elif command.startswith("go "):
            move(player, current_room, command.split(" ")[1])

        else:
            print("Unknown command.")

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
    player.current_room = config.rooms[0].name

    game_loop(config, player)

if __name__ == "__main__":
    main()
