
![dans_dungeon_banner](https://github.com/user-attachments/assets/a7ed793d-785b-45c4-94ee-f45493131001)

# Dan's Dungeon

A dungeon crawler engine written in Python.

## Playing

Run:

`python game.py games/dan.json`

## Creating your own dungeon

First, copy the default JSON file to a file of your choice. Example:

`cp games/dan.json games/mygame.json`

Open the JSON file and modify the details, loot, rooms, and monsters.

Run your game:

`python game.py games/mygame.json`

## Limitations

* All rooms must have a unique name
* Player always starts in the first room defined in the JSON "rooms" array
* Player may only carry one weapon and one armor item at a time

## Example output

```
Game loaded!

Name        : Dan's Dungeon
Description : An example game where you explore a dungeon and fight monsters.
Version     : 1.0.0

Type 'help' for commands.

You are in: Entrance Hall

> look

You are in a dimly lit hall.

Exits:
  North: Dank Hallway

You see a Wooden Box

You are in: Entrance Hall

> open wooden box
You open the Wooden Box and find loot!

You found Steel Sword

You are in: Entrance Hall

> _
```

## License

[MIT](https://mit-license.org)
