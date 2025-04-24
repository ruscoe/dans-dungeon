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
    starting_weapon = LootItem(**data['starting_weapon'])
    starting_armor = LootItem(**data['starting_armor'])

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

    return GameConfig(details=details, starting_weapon=starting_weapon, starting_armor=starting_armor, loot=loot, rooms=rooms)

def help():
    print("stats                          : Show your stats")
    print("look                           : Look around")
    print("go north / south / east / west : Move in a direction")
    print("open <chest_name>              : Open a chest")
    print("fight                          : Fight a monster")
    print("quit                           : Exit game\n")

def stats(player: Player):
    print(f"Health : {player.health}")
    print(f"Gold   : {player.gold}")
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
            if monster.health > 0:
                print(f"You see a {monster.name} (HP: {monster.health}, DMG: {monster.damage})\n")
            else:
                print(f"You see a defeated {monster.name}.\n")

def move(player: Player, room: Room, direction: str):
    if direction in room.exits:
        destination = room.exits[direction]
        player.current_room = destination
        print(f"You go {direction} to {destination}.\n")
    else:
        print("You can't go that way.\n")

def open_chest(chest: Chest):
    if chest.opened:
        print(f"The {chest.name} is already opened.\n")
    else:
        chest.opened = True
        print(f"You open the {chest.name} and find loot!\n")
        return True
    return False

def fight(player: Player, monster: Monster):
    # Check if the monster is alive.
    if monster.health <= 0:
        print(f"The {monster.name} has already been defeated!\n")
        return

    # Player attacks the monster.
    print(f"You attack the {monster.name} for {player.weapon.damage} damage.\n")
    monster.health -= player.weapon.damage
    if monster.health <= 0:
        print(f"You defeated the {monster.name}!\n")
        print(f"You gained {monster.gold} gold!\n")
        player.gold += monster.gold
    else:
        # Monster attacks back.
        if monster.health > 0:
            print(f"The {monster.name} attacks you for {monster.damage} damage.\n")

            # Check if the player has armor.
            if player.armor:
                damage_taken = max(0, monster.damage - player.armor.defense)
                print(f"Your armor absorbs {monster.damage - damage_taken} damage.\n")
            else:
                damage_taken = monster.damage

            player.health -= damage_taken

def game_loop(config: GameConfig, player: Player):
    rooms_by_name = {room.name: room for room in config.rooms}

    while True:
        # Check if the player is alive.
        if player.health <= 0:
            print("You have been defeated! Game over.\n")
            break

        current_room = rooms_by_name.get(player.current_room)

        # Get the player's command.
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
            # Check if the chest exists in the current room.
            if current_room.chests:
            # Split command by the first space to get the chest name.
                parts = command.split(' ', 1)
                chest_name = parts[1].strip().lower()

                for chest in current_room.chests:
                    if chest.name.lower() == chest_name:
                        if (open_chest(chest)):
                            # Give the player some random loot.
                            loot = config.loot
                            if loot:
                                loot_item = random.choice(loot)
                                print(f"You found {loot_item.name}\n")

                                # Handle armor loot.
                                if loot_item.type == "armor":
                                    if player.armor:
                                        print(f"Replace your {player.armor.name} (DEF: {player.armor.defense}) with {loot_item.name} (DEF: {loot_item.defense}) ?\n")
                                        replace = input("Y/N > ").strip().lower()
                                        if replace == "y":
                                            player.armor = loot_item
                                    else:
                                        player.armor = loot_item

                                # Handle weapon loot.
                                elif loot_item.type == "weapon":
                                    if player.weapon:
                                        print(f"Replace your {player.weapon.name} (DMG: {player.weapon.damage}) with {loot_item.name} (DMG: {loot_item.damage})?\n")
                                        replace = input("Y/N > ").strip().lower()
                                        if replace == "y":
                                            player.weapon = loot_item
                                    else:
                                        player.weapon = loot_item

        # Fight a monster.
        elif command.startswith("fight "):
            # Check if there are monsters
            if current_room.monsters:
                # Split command by the first space to get the monster name.
                parts = command.split(' ', 1)
                monster_name = parts[1].strip().lower()
                for monster in current_room.monsters:
                    if monster.name.lower() == monster_name:
                        print(f"You engage the {monster.name} in battle!\n")
                        fight(player, monster)
                        break
            else:
                print("No monsters to fight here.\n")

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

    starting_weapon = config.starting_weapon
    starting_armor = config.starting_armor

    player = Player(health=100, gold=0, armor=starting_armor, weapon=starting_weapon)
    player.current_room = config.rooms[0].name

    print(f"You are in: {player.current_room}\n")

    game_loop(config, player)

if __name__ == "__main__":
    main()
