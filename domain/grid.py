#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    grid.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:38:19 by maprunty         #+#    #+#              #
#    Updated: 2026/09/05 23:39:11 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Grid class to represent a 2D grid of Cell instances."""

from collections.abc import Generator

from .models import DroneMap, Zone
from .vector import Vec2


class Grid:
    """Class to represent a 2D grid of None|Zone instances."""

    def __init__(self, dimensions: Vec2, offset: Vec2) -> None:
        """Initialize the grid with the given width and height."""
        print(
            f"Creating grid with dimensions {dimensions} and offset {offset}"
        )
        self.dimensions = dimensions
        self.offset = offset
        self.fill_empty_grid()

    def __getitem__(self, pos: Vec2 | tuple[int, int]) -> Zone | None:
        """Return the cell at the given position."""
        x, y = self.to_index(pos)
        print(x, y, pos)
        if not self.isvalid((x, y)):
            raise IndexError(f"Key {x, y, pos} is out of bounds")
        return self.grid[y][x]

    def __setitem__(self, pos: Vec2 | tuple[int, int], zone: Zone) -> None:
        """Set the cell at the given position."""
        x, y = self.to_index(pos)
        if not self.isvalid((x, y)):
            raise IndexError(f"Key {x, y, pos} is out of bounds")
        self.grid[y][x] = zone

    def __iter__(self) -> Generator[Zone, None, None]:
        """Iterate over all cells in the grid."""
        for row in self.grid:
            for cell in row:
                if cell is not None:
                    yield cell

    def __repr__(self) -> str:
        """An evalutable string representation of a Grid instance."""
        cls = self.__class__.__name__
        return f"{cls}(width={self.width}, height={self.height})"

    def __str__(self) -> str:
        """Return a string representation of the grid."""
        r_str = ""
        for y in range(self.height):
            for x in range(self.width):
                r_str += f"{x + self.offset.x},{y + self.offset.y} "
                r_str += " "
            r_str += "\n"
        r_str += "\n"
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    r_str += f"{cell.name} at {x},{y}  "
            r_str += "\n"
        return r_str

    @property
    def width(self) -> int:
        """Return the width of the grid."""
        return self.dimensions.x

    @property
    def height(self) -> int:
        """Return the height of the grid."""
        return self.dimensions.y

    @classmethod
    def from_map(cls, drone_map: DroneMap) -> "Grid":
        """Create a grid from a drone map."""
        grid = cls(drone_map.dimensions, drone_map.get_offset())
        for zone in drone_map.adj:
            grid[zone.loc] = zone
        print(grid)
        return grid

    def fill_empty_grid(self) -> None:
        """Fill the grid with None values."""
        print(f"Creating grid of size {self.width}x{self.height}")
        self.grid = [
            [None for x in range(self.width + 1)]
            for y in range(self.height + 1)
        ]

    def to_index(self, pos: Vec2 | tuple[int, int]) -> tuple[int, int]:
        """Convert a position to a grid index."""
        if isinstance(pos, tuple):
            pos = Vec2(*pos)
        return (pos - self.offset).to_tuple()

    def isvalid(self, pos: Vec2 | tuple[int, int]) -> bool:
        """Return whether a world coordinate lies inside the grid."""
        x, y = pos
        return 0 <= x < self.width + 1 and 0 <= y < self.height + 1
