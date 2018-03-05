# MSX museum

![MSX museum start screen](https://github.com/samegens/msxmuseum/blob/master/bootsplash/bootsplash.png?raw=true)

MSX museum for Raspberry Pi, but also running on Windows and non-Pi Linux. 
Written in python, this is a simply a launcher for [openMSX](http://openmsx.org/). 
I call it a museum because of the extra information presented: company, year of release, box shot and screen shot:

![MSX museum F1-Spirit](https://github.com/samegens/msxmuseum/blob/master/images/f1spirit.png?raw=true)

For the best MSX games this information has been collected, the only thing missing are the roms and disk images, because it's not legal to distribute them.

## How to set up

1. Clone this repository.
2. Install the [latest python 3 version](https://www.python.org/downloads/).
3. Install the [latest openMSX version](http://openmsx.org/).
4. In openmsx.bat (Windows) or openmsx.sh (non-Windows) and change the path to openmsx.exe.
5. Get roms or images of the games. Put them in the appropriate directory of the games directory within this repository. 
Supported formats are rom, dsk and zip. The game file should be called game.rom, game.dsk or game.zip.
6. Start msxmuseum.py.

## How to turn this into a permanent museum on a Raspberry Pi

1. You need at least a Raspberry Pi 3 because of its performance. An older version might work but some games will not run smoothly.
2. Install the [latest Raspbian](https://thepi.io/how-to-install-raspbian-on-the-raspberry-pi/), minimal (non-GUI) version is ok.
3. Install pygame and openMSX:

```
sudo apt-get install python-pygame
sudo apt-get install openmsx
````

4. Make sure you're able to put files on the RPi, either using ssh/sftp, USB-stick or by downloading from the network.
5. Clone or copy this repository to the pi home directory, in this example I assume the repository is located in `/home/pi/msxmuseum`.
6. Automatically run the MSX museum on startup. 
7. Optional: change the boot screen of the Rpi to the supplied bootscreen (`/home/pi/msxmuseum/bootsplash/bootsplash.png`), so [this page](http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/custom-boot-up-screen) for instructions.
8. Run `sudo raspi-config` and change the bootup options to 'Console Autologin'.
9. Add this at the bottom of `/home/pi/.bashrc`:

```
if [ `tty` = "/dev/tty1" ]; then
  clear
  echo Loading MSXMuseum
  cd msxmuseum
  python msxmuseum.py
fi
```

10. Reboot, on boot the MSX museum boot splash should be displayed and after that the application should be automatically started.

## Keys

In menu:

- up/down: select a game,
- letter: select the next game with that letter,
- SHIFT+letter: select the previous game with that letter,
- space/enter: launch game,
- ESC: quit MSX museum.

In game:

- F12: toggle full screen,
- ALT+F4: return to menu,
- PrtScn: make a screenshot,
- ALT+F8: save current state,
- ALT+F7: load saved state.

See the [openMSX User's Manual](http://openmsx.org/manual/user.html#keymapping) for more shortcuts.

## Controller

A controller can be plugged in. I used an old PS2 controller with an adapter to USB. The openMSX settings have been configured for this setup. If you need to change it, modify `script.rpi`.

In menu:

- up/down: select a game,
- X: launch game.

In game:

- START: open openMSX menu (choose  'Exit openMSX' to return to the menu),
