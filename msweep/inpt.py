#!/usr/bin/env python3

import sys, tty, termios
import atexit
import time

from datetime import datetime
from queue import Queue, Empty
from enum import Enum

from . import magic_thread


# Originally taken from here: http://stackoverflow.com/a/510364
class GetchUnix:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)
        mode = tty.tcgetattr(self.fd)
        mode[tty.OFLAG] = mode[tty.OFLAG] | tty.OPOST
        tty.tcsetattr(self.fd, tty.TCSAFLUSH, mode)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
        return True

    def __call__(self):
        ch = sys.stdin.read(1)
        return ch


getch = GetchUnix()
atexit.register(lambda: getch.__exit__())

__iota = -5555


def iota():
    global __iota
    i = __iota
    __iota += 1
    return i


KEY_DOWN = iota()
KEY_UP = iota()
KEY_LEFT = iota()
KEY_RIGHT = iota()
KEY_ENTER = iota()

_KEYMAP = {
    '\r' : KEY_ENTER,
    '\033': {
        '[': {
            'A': KEY_UP,
            'B': KEY_DOWN,
            'D': KEY_LEFT,
            'C': KEY_RIGHT
        }
    }
}

ARROW_KEYS = set([KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT])


def keymap(buf):
    curmap = _KEYMAP
    for b in buf:
        if b in curmap:
            curmap = curmap[b]
        else:
            return None
    if isinstance(curmap, dict):
        if "" in curmap:
            return curmap['']
        else:
            return None
    return curmap


@magic_thread.threaded
def stdin_reader(outq):
    while True:
        item = {
            "bytes": [getch()],
            "time": datetime.utcnow(),
        }
        # print("bytes: {}, time: {}".format(item['bytes'], item['time']))
        outq.put(item)


def new_readinput():
    q = Queue(maxsize=0)
    rv = stdin_reader(q)
    return q


def new_time_filter(in_q):
    rv = Queue(maxsize=0)

    @magic_thread.threaded
    def time_filter(out_q):
        while True:
            item = in_q.get()
            while True:
                time.sleep(0.003)
                try:
                    second = in_q.get_nowait()
                    item['bytes'] += second['bytes']
                    item['time'] = second['time']
                except Empty:
                    break
            out_q.put(item)

    time_filter(rv)
    return rv


def main():
    inpt = new_time_filter(new_readinput())
    while True:
        k = inpt.get()
        print("bytes: {}, time: {}".format(k['bytes'], k['time']))
        if k['bytes'] == [chr(3)]:
            print('Recieved CTRL-C, exiting!')
            break


if __name__ == "__main__":
    main()
