# MSX museum

![MSX museum start screen](https://github.com/samegens/msxmuseum/blob/master/bootsplash/bootsplash.png?raw=true)

MSX museum for Raspberry Pi, but also running on Windows and non-Pi Linux. 
Written in python, this is a simply a launcher for [openMSX](http://openmsx.org/). 
I call it a museum because of the extra information presented: company, year of release, box shot and screen shot.
For the best MSX games this information has been collected, the only thing missing are the roms and disk images, because it's not legal to distribute them.

## How to set up

1. Clone this repository.
2. Install the [latest python 3 version](https://www.python.org/downloads/).
3. Install the [latest openMSX version](http://openmsx.org/).
4. In openmsx.bat (Windows) or openmsx.sh (non-Windows) and change the path to openmsx.exe.
5. Get roms or images of the games. Put them in the appropriate directory of the games directory within this repository. 
Supported formats are rom, dsk and zip. The game file should be called game.rom, game.dsk or game.zip.
6. Start msxmuseum.py.

## Keys

In menu:

- up/down: select a game,
- letter: select the next game with that letter,
- SHIFT+letter: select the previous game with that letter.

In game:

- F12: toggle full screen,
- ALT+F4: return to menu,
- PrtScn: make a screenshot,
- ALT+F8: save current state,
- ALT+F7: load saved state.

See the [openMSX User's Manual](http://openmsx.org/manual/user.html#keymapping) for more shortcuts.

