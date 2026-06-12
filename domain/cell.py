#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    cell.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/11 09:07:39 by maprunty         #+#    #+#              #
#    Updated: 2026/06/12 01:31:33 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Cell and Dir classes for maze generation and pathfinding."""

from collections.abc import Iterator
from enum import IntFlag

from .vector import Vec2


class Cell:
    """Cell class has a location and a wall attribute.

    The wall is a 4-bit represantaion. i.e
    0000 has all walls
    0100 has one opening to south
    Args:
        loc (Vec2): The location of the cell in the grid.

    Returns:
        int: Product of a and b.
    """

    N = Dir.N
    E = Dir.E
    S = Dir.S
    W = Dir.W

    def __init__(self, loc: Vec2):
        """Init a cell with a Vec2 location and all walls."""
        self.wall = Dir.A
        self.loc = loc
        self.ispath = False
        self.ispic = False
        self.visited = False

    def debug(self) -> str:
        """Debug string representation of a Cell instance."""
        r_str = ""
        for k, v in vars(self).items():
            r_str += f"{k}:{v} "
        return r_str

    def __repr__(self) -> str:
        """An evalutable string representation of a Cell instance."""
        cls = self.__class__.__name__
        r_str = f"{cls}({self.loc})"
        return r_str

    def __str__(self) -> str:
        """String representation of a Cell instance."""
        r_str = f"{self.loc} "
        r_str += f"{vars(self)}"
        return r_str

    def __sub__(self, other: "Cell") -> Dir:
        """Subtract two cells to get the direction from self to other."""
        if abs(self.loc - other.loc) != 1:
            raise ValueError("Cells are not adjacent")
        return Dir.from_vec(other.loc - self.loc)

    def __iter__(self) -> Iterator[float | int]:
        """Iterate over the fields of a Vec2 instance."""
        return iter((self.x, self.y))

    @property
    def loc(self) -> Vec2:
        """Return the location of a Cell instance as a Vec2."""
        return self._loc

    @loc.setter
    def loc(self, value: Vec2) -> None:
        """Set the location of a Cell instance and update x and y."""
        self.x, self.y = value
        self._loc = value

    @property
    def visited(self) -> bool:
        """Return the visited status of a Cell instance."""
        return self._visited

    @visited.setter
    def visited(self, value: bool) -> None:
        """Set the visited status of a Cell instance."""
        self._visited = value

    def has_wall(self, direction: Dir) -> Dir:
        """Check if a wall exists in the given direction."""
        return self.wall & direction

    def add_wall(self, direction: Dir) -> None:
        """Add a wall in the given direction."""
        self.wall |= direction

    def rm_wall(self, direction: Dir) -> None:
        """Remove a wall in the given direction."""
        self.wall &= ~direction
