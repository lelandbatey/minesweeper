#!/usr/bin/env python3

from pprint import pprint
from enum import Enum
import random

from . import colors


class Contents(object):
    flag = " ⚑ "
    bomb = " 💣 "
    empty = "   "
    smile = " ☺ "


class MineField(object):
    def __init__(self, width=9, height=9, bomb_count=None):
        self.width = width
        self.height = height
        self.bomb_count = bomb_count
        self.board = [
            [Cell(w, h, width, height, self) for h in range(0, height)]
            for w in range(0, width)
        ]
        self._populate_bombs()
        self.set_bomb_contacts()

        self.board[0][0].selected = True
        self.brandnew = True

    def _populate_bombs(self):
        if self.bomb_count is None:
            self.bomb_count = int(0.15 * (self.height * self.width))
        count = self.bomb_count
        selectionfuncs = [
            lambda y: not (y % 2),
            lambda y: bool(y % 2),
            lambda y: not (y %3)
        ]
        # random.shuffle(selectionfuncs)
        # yconstraint, xconstraint = selectionfuncs
        yconstraint, xconstraint = random.sample(selectionfuncs*2, 2)
        for x in range(count):
            while True:
                rx, ry = random.randint(0, self.width - 1), random.randint(
                    0, self.height - 1)
                # Don't place mines on even rows
                if random.randint(0, 1):
                    if yconstraint(ry):
                        continue
                    if xconstraint(rx):
                        continue
                c = self.board[rx][ry]
                if c.contents == Contents.empty:
                    c.contents = Contents.bomb
                    break

    def set_bomb_contacts(self):
        """ for all cells in this minefield, calculate # of bomb contacts"""
        self.bomb_count = 0
        for h in range(self.height):
            for w in range(self.width):
                c = self.board[w][h]
                c.bomb_contacts = 0
                if c.contents == Contents.bomb:
                    self.bomb_count += 1
        for h in range(self.height):
            for w in range(self.width):
                self.board[w][h].set_bomb_contacts()

    def selected(self):
        return [self.board[w][h]
                for h in range(self.height) for w in range(self.width)
                if self.board[w][h].selected]

    def create_foothold(self):
        """generally called when the user makes first selection. Clear out any
        bombs within 2 spaces of the existing selection and move them elsewhere
        onto the board. This prevents losing on the first probe and (usually)
        enables a corridor to open up on which the user may begin working
        """
        sel = self.selected()
        cell = sel[0]
        if cell.contents == Contents.bomb:
            cell.contents = Contents.empty
        for adj in cell.get_adjacent():
            if adj.contents == Contents.bomb:
                adj.contents = Contents.empty
        self.set_bomb_contacts()

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
    def __init__(self, x, y, width, height, field):
        self.field = field
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.contents = Contents.empty
        self.selected = False
        self.bomb_contacts = 0
        self.probed = False
        self.flaged = False
        self.transparent = False

    def set_bomb_contacts(self):
        if self.contents == Contents.bomb:
            self.bomb_contacts = -1
            return

        def get(field, loc):
            if loc[0] >= field.width or loc[0] < 0:
                return None
            if loc[1] >= field.height or loc[1] < 0:
                return None
            return field.board[loc[0]][loc[1]]

        touching = [self.above(), self.below(), self.right(), self.left()]
        corner_deltas = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        touching += [
            get(self.field, delt)
            for delt in [[self.x + d[0], self.y + d[1]] for d in corner_deltas]
        ]
        for cell in touching:
            if cell is not None:
                if cell.contents == Contents.bomb:
                    self.bomb_contacts += 1

    def above(self):
        new_pos = [self.x, self.y - 1]
        if new_pos[1] < 0:
            return None
        return self.field.board[new_pos[0]][new_pos[1]]

    def below(self):
        new_pos = [self.x, self.y + 1]
        if new_pos[1] >= self.height:
            return None
        return self.field.board[new_pos[0]][new_pos[1]]

    def right(self):
        new_pos = [self.x + 1, self.y]
        if new_pos[0] >= self.width:
            return None
        return self.field.board[new_pos[0]][new_pos[1]]

    def left(self):
        new_pos = [self.x - 1, self.y]
        if new_pos[0] < 0:
            return None
        return self.field.board[new_pos[0]][new_pos[1]]

    def top_edge(self):
        return self.y == 0

    def right_edge(self):
        return self.x == self.width - 1

    def bottom_edge(self):
        return self.y == self.height - 1

    def left_edge(self):
        return self.x == 0

    def get_adjacent(self):
        """
        Returns a list containing all cells which are adjacent to the provided cell.
        """

        def get(incell, loc):
            x = incell.x + loc[0]
            y = incell.y + loc[1]
            if x >= incell.field.width or x < 0:
                return None
            if y >= incell.field.height or y < 0:
                return None
            return incell.field.board[x][y]

        touching = [self.above(), self.below(), self.right(), self.left()]
        corner_deltas = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        touching += [get(self, delt) for delt in corner_deltas]
        return [x for x in touching if x]

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
        to_display = ""
        fmt = "{{:^{}}}".format(len(Contents.bomb))
        to_display = Contents.empty
        if self.flaged:
            to_display = Contents.flag
        if self.probed:
            if self.contents == Contents.bomb:
                bg = colors.background(colors.COLOR_WHITE, colors.COLOR_RED)
                fill = colors.apply_color(bg, self.contents)
                return fill
            elif self.contents == Contents.smile:
                contents = fmt.format(self.contents)
                colr = nearness_colors(self.bomb_contacts)
                return colors.apply_color(colr, contents)
            fill = fmt.format(self.bomb_contacts)
            colr = nearness_colors(self.bomb_contacts)
            to_display = colors.apply_color(colr, fill)

        if self.selected:
            bg = colors.background(colors.COLOR_WHITE, colors.COLOR_RED)
            return colors.apply_color(bg, to_display)
        if not self.probed:
            if self.transparent:
                to_display = fmt.format(self.contents)
            bg = colors.background(colors.COLOR_BLACK, colors.COLOR_WHITE)
            return colors.apply_color(bg, to_display)

        return to_display


def nearness_colors(contacts):
    if contacts == -1:
        return colors.background(colors.COLOR_BLACK, colors.COLOR_GREEN_BRIGHT)
    elif contacts == 0:
        return colors.COLOR_BLACK
    elif contacts == 1:
        return colors.COLOR_GREEN_BRIGHT
    elif contacts == 2:
        return colors.COLOR_CYAN_BRIGHT
    elif contacts == 3:
        return colors.COLOR_YELLOW
    elif contacts >= 4:
        return colors.COLOR_MAGENTA_BRIGHT
    else:
        return colors.COLOR_WHITE


if __name__ == '__main__':
    m = MineField(width=12, height=6)
    print(m)
