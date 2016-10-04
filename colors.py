
import re

def remove_color(instr):
    """Returns the given string with all color escape sequences removed."""
    return re.sub(r'\x1b\[[0-9;]*m','', instr)

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

def black(instr):
    return COLOR_BLACK + instr + COLOR_RESET
def red(instr):
    return COLOR_RED + instr + COLOR_RESET
def green(instr):
    return COLOR_GREEN + instr + COLOR_RESET
def yellow(instr):
    return COLOR_YELLOW + instr + COLOR_RESET
def blue(instr):
    return COLOR_BLUE + instr + COLOR_RESET
def magenta(instr):
    return COLOR_MAGENTA + instr + COLOR_RESET
def cyan(instr):
    return COLOR_CYAN + instr + COLOR_RESET
def white(instr):
    return COLOR_WHITE + instr + COLOR_RESET

