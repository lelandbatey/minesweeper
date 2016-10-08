import re


def remove_color(instr):
    """Returns the given string with all color escape sequences removed."""
    return re.sub(r'\x1b\[[0-9;]*m', '', instr)


def extract_colornum(color):
    ccode = re.search('\[3(.*?)m', color)
    ccode = ccode.groups()[0].split(';')[0]
    return ccode


def background(fg_color, bg_color):
    fg_code = extract_colornum(fg_color)
    bg_code = extract_colornum(bg_color)
    return "\x1b[3{}m\x1b[4{}m".format(fg_code, bg_code)


COLOR_RESET = "\x1b[0m"
COLOR_BLACK = "\x1b[30m"
COLOR_RED = "\x1b[31m"
COLOR_GREEN = "\x1b[32m"
COLOR_YELLOW = "\x1b[33m"
COLOR_BLUE = "\x1b[34m"
COLOR_MAGENTA = "\x1b[35m"
COLOR_CYAN = "\x1b[36m"
COLOR_WHITE = "\x1b[37m"

COLOR_BLACK_BRIGHT = "\x1b[30;1m"
COLOR_RED_BRIGHT = "\x1b[31;1m"
COLOR_GREEN_BRIGHT = "\x1b[32;1m"
COLOR_YELLOW_BRIGHT = "\x1b[33;1m"
COLOR_BLUE_BRIGHT = "\x1b[34;1m"
COLOR_MAGENTA_BRIGHT = "\x1b[35;1m"
COLOR_CYAN_BRIGHT = "\x1b[36;1m"
COLOR_WHITE_BRIGHT = "\x1b[37;1m"


def apply_color(color, instr):
    return color + instr + COLOR_RESET


def black(instr):
    return apply_color(COLOR_BLACK, instr)


def red(instr):
    return apply_color(COLOR_RED, instr)


def green(instr):
    return apply_color(COLOR_GREEN, instr)


def yellow(instr):
    return apply_color(COLOR_YELLOW, instr)


def blue(instr):
    return apply_color(COLOR_BLUE, instr)


def magenta(instr):
    return apply_color(COLOR_MAGENTA, instr)


def cyan(instr):
    return apply_color(COLOR_CYAN, instr)


def white(instr):
    return apply_color(COLOR_WHITE, instr)
