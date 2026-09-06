#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    main.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/11 15:24:56 by maprunty         #+#    #+#              #
#    Updated: 2026/09/06 09:38:50 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import glob
import os
import sys

from display import ConsoleDisplay, Display, NCursesDisplay
from parser import Parser

DISPLAYS = [ConsoleDisplay, NCursesDisplay]


def list_files_recursive(path="."):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            list_files_recursive(full_path)
        else:
            print(full_path)


def list_files_glob(pattern="./**/*", recursive=True):
    files = glob.glob(pattern, recursive=recursive)
    return [file for file in files]


def get_display() -> type[Display]:
    choice = int(
        input(
            "Choose a display:\n"
            + "\n".join([f"{i}. {j.__name__}" for i, j in enumerate(DISPLAYS)])
            + f"\nEnter a number between 0 and {len(DISPLAYS)}: "
        )
    )
    if not choice.isdigit():
        print("Invalid input. Please enter a number.")
        return get_map()
    if choice >= 0 and choice <= len(DISPLAYS):
        return DISPLAYS[choice]
    return get_display()


MAPS = list_files_glob("./maps/**/*.txt")


def get_map() -> str:
    directory_path = "./maps"
    choice = input(
        "Choose a map:\n"
        + "\n".join([f"{i}. {j}" for i, j in enumerate(MAPS)])
        + f"\nEnter a number between 0 and {len(MAPS)}: "
    )
    if not choice.isdigit():
        print("Invalid input. Please enter a number.")
        return get_map()
    i_choice = int(choice)
    if i_choice >= 0 and i_choice <= len(MAPS):
        return MAPS[choice]
    return get_map()


def main_loop():
    while True:
        display = get_display()
        map_file = get_map()
        dm = Parser().parse_file(map_file)
        display(dm).run()
        sys.stdout.flush()
        key = input("Press 'q' to quit or 'enter' to go again: ")
        if key in ("q", chr(27)):
            break


if __name__ == "__main__":
    main_loop()
