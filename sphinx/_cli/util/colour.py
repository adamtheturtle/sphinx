"""Format coloured console output."""

from __future__ import annotations

import os
import sys
from collections.abc import Callable  # NoQA: TCH003

if sys.platform == 'win32':
    import colorama


_COLOURING_DISABLED = True


def terminal_supports_colour() -> bool:
    """Return True if coloured terminal output is supported."""
    if 'NO_COLOUR' in os.environ or 'NO_COLOR' in os.environ:
        return False
    if 'FORCE_COLOUR' in os.environ or 'FORCE_COLOR' in os.environ:
        return True

    try:
        if not sys.stdout.isatty():
            return False
    except (AttributeError, ValueError):
        # Handle cases where .isatty() is not defined, or where e.g.
        # "ValueError: I/O operation on closed file" is raised
        return False

    # Do not colour output if on a dumb terminal
    return os.environ.get('TERM', 'unknown').lower() not in {'dumb', 'unknown'}


def disable_colour() -> None:
    global _COLOURING_DISABLED
    _COLOURING_DISABLED = True
    if sys.platform == 'win32':
        colorama.deinit()


def enable_colour() -> None:
    global _COLOURING_DISABLED
    _COLOURING_DISABLED = False
    if sys.platform == 'win32':
        colorama.init()


def colourise(colour_name: str, text: str, /) -> str:
    if _COLOURING_DISABLED:
        return text
    return globals()[colour_name](text)


def _create_colour_func(escape_code: str, /) -> Callable[[str], str]:
    def inner(text: str) -> str:
        if _COLOURING_DISABLED:
            return text
        return f'\x1b[{escape_code}m{text}\x1b[39;49;00m'
    return inner


reset = _create_colour_func('39;49;00')
bold = _create_colour_func('01')
faint = _create_colour_func('02')
standout = _create_colour_func('03')
underline = _create_colour_func('04')
blink = _create_colour_func('05')

black = _create_colour_func('30')
darkred = _create_colour_func('31')
darkgreen = _create_colour_func('32')
brown = _create_colour_func('33')
darkblue = _create_colour_func('34')
purple = _create_colour_func('35')
turquoise = _create_colour_func('36')
lightgray = _create_colour_func('37')

darkgray = _create_colour_func('90')
red = _create_colour_func('91')
green = _create_colour_func('92')
yellow = _create_colour_func('93')
blue = _create_colour_func('94')
fuchsia = _create_colour_func('95')
teal = _create_colour_func('96')
white = _create_colour_func('97')
