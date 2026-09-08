#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    base_display.py                                   :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/09/06 11:26:29 by maprunty         #+#    #+#              #
#    Updated: 2026/09/06 11:37:00 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


from abc import ABC, abstractmethod

from domain import Connection, DroneMap, Grid, Zone

FrameEntry = Zone | Connection | None


class Display(ABC):
    def __init__(self, drone_map: DroneMap) -> None:
        self.drone_map = drone_map
        self.grid = Grid.from_map(drone_map)
        self.width = self.grid.width
        self.height = self.grid.height

    def build(self) -> list[list[FrameEntry]]:
        frame: list[list[FrameEntry]] = [
            [None for _ in range(self.width * 2)]
            for _ in range(self.height * 2)
        ]

        for y in range(self.height):
            for x in range(self.width):
                wx, wy = (x * 2, y * 2)
                cell = self.grid[(x, y)]
                if cell is None:
                    continue
                for conn in self.drone_map.adj[cell]:
                    if cell != conn.a:
                        continue
                    d = conn.b.loc - conn.a.loc
                    frame[wy + d.y][wx + d.x] = conn
                frame[wy][wx] = cell
        return frame

    def _color_for(self, entry: FrameEntry) -> str | None:
        """Color name for a frame entry, if any. Universal across backends."""
        if entry is None:
            return None
        if isinstance(entry, Connection):
            return entry.a.color
        return entry.color

    @abstractmethod
    def render(self) -> None:
        """Draw the current frame. Every concrete backend implements this."""
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        """Run the display loop. Every concrete backend implements this."""
        raise NotImplementedError
