"""
Dan's Dungeon

A JSON-based game engine for a text-based dungeon crawlers.

Usage:
    python game.py <path_to_game_json_file>
"""

import sys
import json
import random
from models import Chest, Details, LootItem, Monster, Player, Room, GameConfig

def parse_game_config(data: dict) -> GameConfig:
    details = Details(**data['details'])

    loot = [LootItem(**item) for item in data.get('loot', [])]

    rooms = []
    for room in data.get('rooms', []):
        room_obj = Room(
            name=room['name'],
            description=room['description'],
            exits=room['exits'],
            chests=[Chest(**chest) for chest in room.get('chests', [])],
            monsters=[Monster(**m) for m in room.get('monsters', [])]
        )
        rooms.append(room_obj)

    return GameConfig(details=details, loot=loot, rooms=rooms)

def help():
    print("look                           : Look around")
    print("go north / south / east / west : Move in a direction")
    print("open <chest_name>              : Open a chest")
    print("fight                          : Fight a monster")
    print("quit                           : Exit game\n")

def look(room: Room):
    print(f"\n{room.description}\n")
    print("Exits:")
    for direction, destination in room.exits.items():
        print(f"  {direction.title()}: {destination}")
    if room.chests:
        for chest in room.chests:
            print(f"You see a {chest.name}")
    if room.monsters:
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

        if command == "look":
            look(current_room)

        elif command.startswith("go "):
            move(player, current_room, command.split(" ")[1])

        elif command.startswith("open "):
            # Split command by the first space to get the chest name.
            parts = command.split(' ', 1)
            if len(parts) < 2:
                print("Please specify a chest name.")
                continue
            chest_name = parts[1].strip().lower()

            # Check if the chest exists in the current room.
            for chest in current_room.chests:
                if chest.name.lower() == chest_name:
                    if chest.opened:
                        print(f"The {chest.name} is already opened.")
                    else:
                        chest.opened = True
                        print(f"You open the {chest.name} and find loot!")

                        # Give the player some random loot.
                        loot = config.loot
                        if loot:
                            loot_item = random.choice(loot)
                            print(f"You found {loot_item.name}")

        elif command == "help":
            help()

        elif command == "quit":
            print("Goodbye!")
            break

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
    print("Type 'help' for commands.\n")

    player = Player(health=100, defense="", weapon="")
    player.current_room = config.rooms[0].name

    game_loop(config, player)

if __name__ == "__main__":
    main()
