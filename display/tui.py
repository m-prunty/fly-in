#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    tui.py                                            :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/11 15:27:23 by maprunty         #+#    #+#              #
#    Updated: 2026/06/13 06:22:01 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from typing import Protocol

from domain import DroneMap, Grid
from simulation import MoveEvent, Simulation


class Display(Protocol):
    def render(self, sim: Simulation) -> None: ...
    def on_event(self, event: MoveEvent) -> None: ...


class TuiDisplay:
    def __init__(self, drone_map: DroneMap):
        self._grid = Grid.from_map(drone_map)

    def render(self):
        print("Rendering TUI...")
        adj_sorted = sorted(self.drone_map.adj, key=lambda z: (z.y, z.x))
        y_curr = min(z.y for z in adj_sorted)
        line_str = "|"
        while adj_sorted:
            current = adj_sorted.pop(0)
            line_str += " " * (current.x - len(line_str))
            if current == self.drone_map.start_zone:
                line_str += "S"
            elif current == self.drone_map.end_zone:
                line_str += "E"
            else:
                line_str += "H"
            if adj_sorted and adj_sorted[0].y > y_curr:
                print(line_str)
                line_str = "|"
                y_curr = adj_sorted[0].y
