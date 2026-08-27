#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    grid.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:38:19 by maprunty         #+#    #+#              #
#    Updated: 2026/08/27 18:39:05 by maprunty        ###   ########.fr        #
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
        self.dimensions = dimensions
        self.offset = offset
        self.fill_empty_grid()

    @property
    def width(self) -> int:
        """Return the width of the grid."""
        return self.dimensions.x + self.offset.x

    @property
    def height(self) -> int:
        """Return the height of the grid."""
        return self.dimensions.y + self.offset.y

    def fill_empty_grid(self) -> None:
        """Fill the grid with None values."""
        print(f"Creating grid of size {self.width}x{self.height}")
        self.grid = [
            [None for x in range(self.width)] for y in range(self.height)
        ]

    def to_index(self, pos: Vec2 | tuple[int, int]) -> tuple[int, int]:
        """Convert a position to a grid index."""
        if isinstance(pos, tuple):
            pos = Vec2(*pos)
        print(f"{pos} - {self.offset} = {pos - self.offset}")
        return (pos - self.offset).to_tuple()

    def isvalid(self, pos: Vec2 | tuple[int, int]) -> bool:
        """Return whether a world coordinate lies inside the grid."""
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    @classmethod
    def from_map(cls, drone_map: DroneMap) -> "Grid":
        """Create a grid from a drone map."""
        grid = cls(drone_map.dimensions, drone_map.offset)
        print(grid)
        for zone in drone_map.adj:
            grid[zone.loc] = zone
        return grid

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
        self[(x, y)] = zone

    def __str__(self) -> str:
        """Return a string representation of the grid."""
        return "\n".join(
            [
                " ".join(
                    [f"{x},{y}: {self[(x, y)]}" for x in range(self.width)]
                )
                for y in range(self.height)
            ]
        )

    def __iter__(self) -> Generator[Zone, None, None]:
        """Iterate over all cells in the grid."""
        for y in self.grid:
            if isinstance(y, Zone):
                yield y

    def __repr__(self) -> str:
        """An evalutable string representation of a Grid instance."""
        cls = self.__class__.__name__
        return f"{cls}(width={self.width}, height={self.height})"
