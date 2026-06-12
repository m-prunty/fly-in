#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    grid.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:38:19 by maprunty         #+#    #+#              #
#    Updated: 2026/06/12 05:39:48 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Grid class to represent a 2D grid of Cell instances."""

from collections.abc import Generator

from .models import Zone
from .vector import Vec2


class Grid:
    """Grid class has a width, height, and a 2D list of Cell instances."""

    def __init__(self, width: int, height: int):
        """Init a grid with the given width and height of Cell instances."""
        self.width, self.height = width, height
        self.fill_empty_grid()

    def fill_empty_grid(self) -> None:
        """Fill a grid with empty Cell instances."""
        print(f"Creating grid of size {self.width}x{self.height}")
        self.grid = [
            [None for x in range(self.width)] for y in range(self.height)
        ]

    def isvalid(self, v: Vec2 | tuple[int, int] | Zone) -> bool:
        """Check if a Vec2 instance is within the bounds of the grid."""
        if isinstance(v, tuple):
            v = Vec2(*v)
        return (
            v.x is not None
            and v.y is not None
            and 0 <= v.x < self.width
            and 0 <= v.y < self.height
        )

    def __getitem__(self, key: tuple[int, int] | Vec2 | Zone) -> Zone:
        """Get a cell from the grid using a tuple of (x, y) or a Vec2 instance.

        Where th key is out of bounds, return a Zone with location (0,0)
        and all walls.
        """
        try:
            if self.isvalid(key):
                x, y = key
                z = self.grid[int(y)][int(x)]
                if z is not None:
                    return z
            raise IndexError(f"Key {key} is out of bounds")
        except Exception:
            return Zone(None, Vec2(0, 0))

    def __iter__(self) -> Generator[Zone, None, None]:
        """Iterate over all cells in the grid."""
        for y in self.grid:
            yield from y

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


class Graph(Protocol):
    """Graph protocol for maze generation and pathfinding."""

    grid: Grid

    def edges(self, cell: Cell) -> Iterable[Edge]:
        """Returns list of edges of cell."""
        ...


class GridGraph:
    """Graph for maze generation.

    Returns all neighbours of cell, even if wall between them.
    """

    def __init__(self, grid: Grid) -> None:
        """Initializes GenGraph with a grid."""
        self.grid = grid

    def edges(self, cell: Cell) -> Iterable[Edge]:
        """Returns list of edges of cell."""
        cell_nb = self.grid.neighbour(cell)
        for _, nb in cell_nb.items():
            yield Edge(cell, nb)
