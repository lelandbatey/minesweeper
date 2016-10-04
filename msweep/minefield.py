#!/usr/bin/env python3

from pprint import pprint
from enum import Enum
import random

from . import colors

class Contents(object):
    flag = "⚑ "
    bomb = " 💣 "
    empty = "   "



class MineField(object):
    def __init__(self, width=9, height=9):
        self.width = width
        self.height = height
        self.board = [[Cell(w, h, width, height) for h in range(0, height)]
                      for w in range(0, width)]
        self._populate_bombs()
        self.board[0][0].selected = True

    def _populate_bombs(self, count=None):
        if count is None:
            count = int(0.15 * (self.height * self.width))
        for x in range(count):
            while True:
                rx, ry = random.randint(0, self.width - 1), random.randint(
                    0, self.height - 1)
                c = self.board[rx][ry]
                if c.contents == Contents.empty:
                    c.contents = Contents.bomb
                    break
    def selected(self):
        return [self.board[w][h] for h in range(self.height) for w in range(self.width) if self.board[w][h].selected]

    def __str__(self):
        rv = ""
        rows = []
        for h in range(self.height):
            header = ""
            mid = ""
            footer = ""
            for w in range(self.width):
                c = self.board[w][h]
                nh, nm, nl = c.render()
                header += nh
                mid += nm
                footer += nl
            # Only include the footer if it's the bottom row
            tojoin = [header, mid]
            if footer:
                tojoin.append(footer)
            rows.append("\n".join(tojoin))
        return "\n".join(rows)


class Cell(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.contents = Contents.empty
        self.selected = False

    def top_edge(self):
        return self.y == 0

    def right_edge(self):
        return self.x == self.width - 1

    def bottom_edge(self):
        return self.y == self.height - 1

    def left_edge(self):
        return self.x == 0

    def render(self):
        header = ""
        mid = ""
        footer = ""
        me = str(self)
        length = len(colors.remove_color(me))

        if self.top_edge():
            if self.left_edge():
                header += "┌"
            else:
                header += "┬"
        else:
            if self.left_edge():
                header += "├"
            else:
                header += "┼"
        header += "─" * length
        if self.right_edge():
            if self.top_edge():
                header += "┐"
            else:
                header += "┤"

        mid += "│" + me
        if self.right_edge():
            mid += "│"

        if self.bottom_edge():
            if self.left_edge():
                footer += "└"
            else:
                footer += "┴"
            footer += "─" * length
            if self.right_edge():
                footer += "┘"

        return header, mid, footer

    def __str__(self):
        if self.selected:
            bg = colors.background(colors.COLOR_WHITE, colors.COLOR_RED)
            return colors.apply_color(bg, self.contents)
        return self.contents
        # return str((self.x, self.y))


if __name__ == '__main__':
    m = MineField(width=12, height=6)
    print(m)
