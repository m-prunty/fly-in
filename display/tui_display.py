#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    tui_display.py                                    :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/11 15:27:23 by maprunty         #+#    #+#              #
#    Updated: 2026/09/06 11:59:11 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


from __future__ import annotations

import curses

from domain import Connection, DroneMap

from .base_display import Display, FrameEntry

_CURSES_COLORS: dict[str, int] = {
    "black": curses.COLOR_BLACK,
    "red": curses.COLOR_RED,
    "green": curses.COLOR_GREEN,
    "yellow": curses.COLOR_YELLOW,
    "blue": curses.COLOR_BLUE,
    "magenta": curses.COLOR_MAGENTA,
    "cyan": curses.COLOR_CYAN,
    "white": curses.COLOR_WHITE,
}

# curses pair ids start at 1 — 0 is reserved for the default pair.
_COLOR_PAIR_IDS: dict[str, int] = {
    name: i + 1 for i, name in enumerate(_CURSES_COLORS)
}


class AsciiDisplay(Display):
    def _char_for(self, entry: FrameEntry) -> str:
        if entry is None:
            return " "
        if isinstance(entry, Connection):
            return "+"
        if entry == self.drone_map.start_zone:
            return "S"
        if entry == self.drone_map.end_zone:
            return "E"
        return "H"


class ConsoleDisplay(AsciiDisplay):
    def __init__(self, drone_map: DroneMap) -> None:
        super().__init__(drone_map)

    def render(self) -> None:
        frame = self.build()
        for row in frame:
            print("".join(self._char_for(entry) for entry in row))

    def run(self) -> None:
        """Render the map once and block until the user quits with q/Esc."""
        self.render()
        while True:
            key = input("Press 'q' or 'Esc' to quit: ")
            if key in ("q", chr(27)):
                break


class NCursesDisplay(AsciiDisplay):
    """Render DroneMap frames with curses instead of stdout."""

    def __init__(self, drone_map: DroneMap) -> None:
        super().__init__(drone_map)
        self._stdscr: curses.window | None = None

    def render(self) -> None:
        """Draw a single frame. Must run inside run()'s curses session."""
        frame = self.build()

        if self._stdscr is None:
            raise RuntimeError("render() called outside of run()")
        stdscr = self._stdscr
        max_y, max_x = stdscr.getmaxyx()
        stdscr.erase()
        for y, row in enumerate(frame):
            if y >= max_y:
                break
            for x, entry in enumerate(row):
                char = self._char_for(entry)
                if char == " " or x >= max_x:
                    continue
                if y == max_y - 1 and x == max_x - 1:
                    continue
                color = self._color_for(entry)
                pair_id = _COLOR_PAIR_IDS.get((color or "").lower(), 0)
                stdscr.addstr(y, x, char, curses.color_pair(pair_id))
        stdscr.refresh()

    def run(self) -> None:
        """Enter curses mode and block until the user quits with q/Esc."""
        curses.wrapper(self._main_loop)

    def _main_loop(self, stdscr: curses.window) -> None:
        self._stdscr = stdscr
        curses.curs_set(0)  # hide the cursor
        curses.start_color()
        curses.use_default_colors()
        for name, fg in _CURSES_COLORS.items():
            curses.init_pair(_COLOR_PAIR_IDS[name], fg, -1)

        while True:
            self.render()
            key = stdscr.getch()  # blocks until a key is pressed
            if key in (ord("q"), 27):  # q or Esc
                break
