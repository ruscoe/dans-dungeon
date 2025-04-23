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
* Player always stats in the first room defined in the JSON "rooms" array
* Player may only carry one weapon and one armor item at a time

## License

[MIT](https://mit-license.org)
