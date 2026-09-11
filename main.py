#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    main.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/11 15:24:56 by maprunty         #+#    #+#              #
#    Updated: 2026/09/06 11:38:56 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import glob
import sys
from collections.abc import Callable
from typing import TypeVar

from display import ConsoleDisplay, MlxDisplay, NCursesDisplay
from parser import Parser

DISPLAYS = [ConsoleDisplay, NCursesDisplay, MlxDisplay]
MAPS = [file for file in glob.glob("./maps/**/*.txt")]
T = TypeVar("T")


def prompt_choice(
    items: list[T], label: str, display: Callable[[T], str] = str
) -> T:
    prompt = (
        f"Choose a {label}:\n"
        + "\n".join(f"{i}. {display(item)}" for i, item in enumerate(items))
        + f"\nEnter a number between 0 and {len(items) - 1}: "
    )
    while True:
        choice = input(prompt)
        if choice.isdigit() and 0 <= int(choice) < len(items):
            return items[int(choice)]
        if choice.lower() in ("q", "quit", "exit", chr(27)):
            sys.exit(0)
        print("Invalid input. Please enter a number in range.")


def get_display() -> type[T]:
    return prompt_choice(DISPLAYS, "display", lambda d: d.__name__)


def get_map() -> str:
    return prompt_choice(MAPS, "map")


def main_loop():
    while True:
        display = get_display()
        map_file = get_map()
        dm = Parser().parse_file(map_file)
        display(dm).run()
        sys.stdout.flush()
        key = input("Press 'q' to quit or 'enter' to go again: ")
        if key in ("q", "quit", "exit", chr(27)):
            sys.exit(0)


if __name__ == "__main__":
    main_loop()
