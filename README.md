
Minesweeper!
============

A simple implementation of minesweeper in the terminal. Written in Python 3,
using only the standard library, without Curses!

## How do I play right now?

Do this:

	git clone http://git.home.lelandbatey.com/lelandbatey/minesweeper.git
	cd minesweeper/
	./minesweeper -h # To print usage
	./minesweeper

Use arrows to move, the 'enter' key to probe, 'f' to flag, CTRL-C to exit. You
win when you flag all the mines. If you probe a mine then it explodes, you die,
and the program exits.

