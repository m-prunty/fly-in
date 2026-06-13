#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    grid.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:38:19 by maprunty         #+#    #+#              #
#    Updated: 2026/06/13 06:43:59 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Grid class to represent a 2D grid of Cell instances."""

from collections.abc import Generator

from .models import DroneMap, Zone
from .vector import Vec2


class Grid:
    """Class to represent a 2D grid of None|Zone instances."""

    def __init__(self, width: int, height: int, offset: Vec2) -> None:
        """Initialize the grid with the given width and height."""
        self.width, self.height = width, height
        self.offset = offset
        self.fill_empty_grid()

    def fill_empty_grid(self) -> None:
        """Fill the grid with None values."""
        print(f"Creating grid of size {self.width}x{self.height}")
        self.grid = [
            [None for x in range(self.width)] for y in range(self.height)
        ]

    def to_index(self, pos: Vec2 | tuple[int, int]) -> Vec2:
        """Convert a position to a grid index."""
        if isinstance(pos, tuple):
            pos = Vec2(*pos)
        return pos - self.offset

    @classmethod
    def from_map(cls, drone_map: DroneMap) -> "Grid":
        """Create a grid from a drone map."""
        grid = cls(drone_map.width(), drone_map.height())
        for zone in drone_map.adj:
            grid[zone.loc] = zone
        return grid

    def isvalid(self, v: Vec2 | tuple[int, int]) -> bool:
        """Check if a Vec2 instance is within the bounds of the grid."""
        if isinstance(v, tuple):
            v = Vec2(*v)
        return (
            v.x is not None
            and v.y is not None
            and self.offset.x <= v.x < self.width
            and self.offset.y <= v.y < self.height
        )

    def __getitem__(self, key: tuple[int, int] | Vec2) -> Zone:
        """Get a cell from the grid using a tuple of (x, y) or a Vec2 instance.

        Where th key is out of bounds, return a Zone with location (0,0)
        and all walls.
        """
        try:
            if self.isvalid(key):
                x, y = self.to_index(key)
                z = self.grid[int(y)][int(x)]
                if z is not None:
                    return z
            raise IndexError(f"Key {key} is out of bounds")
        except Exception:
            return Zone(None, Vec2(0, 0))

    def __setitem__(self, key: tuple[int, int] | Vec2, value: Zone) -> None:
        """Set a cell in the grid using a tuple of (x, y) or a Vec2 instance."""
        if self.isvalid(key):
            x, y = key
            self.grid[int(y)][int(x)] = value
        else:
            raise IndexError(f"Key {key} is out of bounds")

    def __iter__(self) -> Generator[Zone, None, None]:
        """Iterate over all cells in the grid."""
        for y in self.grid:
            if isinstance(y, Zone):
                yield y

    def __repr__(self) -> str:
        """An evalutable string representation of a Grid instance."""
        cls = self.__class__.__name__
        return f"{cls}(width={self.width}, height={self.height})"


"""
    def __str__(self) -> str:
        r_str = ""
        for x in range(self.width):
            cell = self[x, 0]
            r_str += "+"
            r_str += "---" if cell.has_wall(Dir.N) else "   "
        r_str += "+\n"
        for y in range(self.height):
            for x in range(self.width):
                cell = self[x, y]
                if cell.has_wall(Dir.W):
                    r_str += "|"
                else:
                    r_str += " "

                if cell.ispath:
                    r_str += " ° "
                    print(f"Cell {cell.loc} is in the path")
                elif cell.ispic:
                    r_str += " X "
                    print(f"Cell {cell.loc} is pic")
                else:
                    r_str += "   "
                    print(f"Cell {cell} ")
            r_str += "|\n" if cell.has_wall(Dir.E) else " \n"
            for x in range(self.width):
                cell = self[x, y]
                r_str += "+"
                if cell.has_wall(Dir.S):
                    r_str += "---"
                else:
                    r_str += "   "
            r_str += "+\n"
        r_str += f"Path: {self.path_to_str()}"
        return r_str
"""
