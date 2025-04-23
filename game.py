"""
Dan's Dungeon

A JSON-based game engine for text-based dungeon crawlers.

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
    print("stats                          : Show your stats")
    print("look                           : Look around")
    print("go north / south / east / west : Move in a direction")
    print("open <chest_name>              : Open a chest")
    print("fight                          : Fight a monster")
    print("quit                           : Exit game\n")

def stats(player: Player):
    print(f"Health : {player.health}")
    print(f"Armor  : {player.armor.name} (DEF: {player.armor.defense})") if player.armor else None
    print(f"Weapon : {player.weapon.name} (DMG: {player.weapon.damage})") if player.weapon else None
    print("\n")

def look(room: Room):
    print(f"\n{room.description}\n")
    print("Exits:")
    for direction, destination in room.exits.items():
        print(f"  {direction.title()}: {destination}")
    print ("\n")

    if room.chests:
        for chest in room.chests:
            print(f"You see a {chest.name}\n")

    if room.monsters:
        for monster in room.monsters:
            print(f"{monster.name} (HP: {monster.health}, DMG: {monster.damage})\n")

def move(player: Player, room: Room, direction: str):
    if direction in room.exits:
        destination = room.exits[direction]
        player.current_room = destination
        print(f"You go {direction} to {destination}.\n")
    else:
        print("You can't go that way.\n")

def open_chest(chest_name: str, room: Room):
    # Check if the chest exists in the current room.
    for chest in room.chests:
        if chest.name.lower() == chest_name:
            if chest.opened:
                print(f"The {chest.name} is already opened.\n")
            else:
                chest.opened = True
                print(f"You open the {chest.name} and find loot!\n")
                return True
    return False

def game_loop(config: GameConfig, player: Player):
    rooms_by_name = {room.name: room for room in config.rooms}

    while True:
        current_room = rooms_by_name.get(player.current_room)
        print(f"You are in: {current_room.name}\n")

        # Get the user's command.
        command = input("> ").strip().lower()

        # Show player stats.
        if command == "stats":
            stats(player)

        # Look around.
        elif command == "look":
            look(current_room)

        # Move in a direction.
        elif command.startswith("go "):
            move(player, current_room, command.split(" ")[1])

        # Open a chest.
        elif command.startswith("open "):
            # Split command by the first space to get the chest name.
            parts = command.split(' ', 1)
            if len(parts) < 2:
                print("Please specify a chest name.\n")
                continue
            chest_name = parts[1].strip().lower()

            if (open_chest(chest_name, current_room)):
                # Give the player some random loot.
                loot = config.loot
                if loot:
                    loot_item = random.choice(loot)
                    print(f"You found {loot_item.name}\n")
                    if loot_item.type == "armor":
                        # Handle armor loot.
                        if player.armor:
                            print(f"Replace your {player.armor.name} (DEF: {player.armor.defense}) with {loot_item.name} (DEF: {loot_item.defense}) ?\n")
                            replace = input("Y/N > ").strip().lower()
                            if replace == "y":
                                player.armor = loot_item
                        else:
                            player.armor = loot_item

                    elif loot_item.type == "weapon":
                        # Handle weapon loot.
                        if player.weapon:
                            print(f"Replace your {player.weapon.name} (DMG: {player.weapon.damage}) with {loot_item.name} (DMG: {loot_item.damage})?\n")
                            replace = input("Y/N > ").strip().lower()
                            if replace == "y":
                                player.weapon = loot_item
                        else:
                            player.weapon = loot_item

        # Display commands.
        elif command == "help":
            help()

        # Exit the game.
        elif command == "quit":
            print("Goodbye!\n")
            break

        else:
            print("Unknown command.\n")

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

    starting_armor = LootItem(name="Holey Shield", type="armor", defense=1)
    starting_weapon = LootItem(name="Broken Sword", type="weapon", damage=1)

    player = Player(health=100, armor=starting_armor, weapon=starting_weapon)
    player.current_room = config.rooms[0].name

    game_loop(config, player)

if __name__ == "__main__":
    main()
