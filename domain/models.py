#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    models.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/25 01:27:37 by maprunty         #+#    #+#              #
#    Updated: 2026/06/12 20:25:55 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Zone, Connection, DroneMap dataclasses (the graph data model).

VII.2
Zone Occupancy Rules
• By default, a zone may contain at most one drone at any given simulation turn.
• Zones with max_drones=N metadata can contain up to N drones simultaneously.
• The only special exceptions to occupancy rules are:
◦ The start zone: all drones begin here and may share the space initially.
◦ The end zone: multiple drones can arrive here and are considered delivered.
• Two drones may not enter the same zone on the same turn unless the zone’s capacity
allows it.
• A drone may not move into a zone that would exceed its maximum capacity.
• Connection capacity (max_link_capacity) defined on connections limits how many
drones can traverse the same connection simultaneously.
• Drones may move simultaneously, as long as all capacity constraints are respected.

• Zone types:
◦ normal – Standard zone with 1 turn movement cost (default)
◦ blocked – Inaccessible zone. Drones must not enter or pass through this zone.
Any path using it is invalid.
◦ restricted – A sensitive or dangerous zone. Movement to this zone costs 2
turns.
◦ priority – A preferred zone. Movement to this zone costs 1 turn but should
be prioritized in pathfinding.
"""

from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum
from typing import TypedDict

from .vector import Vec2


class ZoneType(Enum):
    """Define type of a zone, which affects movement cost and accessibility."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class MetaData(TypedDict, total=False):
    """Metadata for a zone, including type and optional max_drones."""

    zone_type: ZoneType
    color: str
    max_drones: int | None
    max_link_capacity: int | None


@dataclass(frozen=True)
class Zone:
    """Represent a zone in the drone map."""

    name: str | None
    loc: Vec2
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return (
            f"Zone(name={self.name}, "
            + f"x={self.x}, "
            + f"y={self.y}, "
            + f"type={self.zone_type.value}, "
            + f"color={self.color}, "
            + f"max_drones={self.max_drones})"
        )

    @property
    def x(self) -> int:
        return int(self.loc.x)

    @property
    def y(self) -> int:
        return int(self.loc.y)

    def __iter__(self) -> Iterator[int]:
        """Allow unpacking a Zone instance as (x, y)."""
        yield self.x
        yield self.y


@dataclass(frozen=True)
class Connection:
    """Represent a connection between two zones, optional capacity."""

    a: Zone
    b: Zone
    max_link_capacity: int = 1


@dataclass
class Transit:
    """Represent a drone in movement between two zones."""

    edge: Connection
    ticks_total: int = 1
    ticks_elapsed: int = 0

    @property
    def progress(self) -> float:
        """Return interpolated progress from 0.0 to 1.0."""
        return self.ticks_elapsed / self.ticks_total

    def advance(self) -> bool:
        """Advance the transit by one tick. Return True if transit is complete."""
        self.ticks_elapsed += 1
        return self.ticks_elapsed >= self.ticks_total


@dataclass
class DroneMap:
    """Represent the drone map, including zones, connections, and metadata."""

    nb_drones: int
    start_zone: Zone
    end_zone: Zone
    adj: dict[Zone, list[Connection]] = field(default_factory=dict)

    def __getitem__(self, zone: Zone) -> list[Connection]:
        return self.adj.get(zone, [])

    def __setitem__(self, zone: Zone, connections: list[Connection]) -> None:
        self.adj[zone] = connections

    def __iter__(self) -> Iterator[Zone]:
        return iter(self.adj)

    def width(self) -> int:
        """Calculate the width of the map based on zone coordinates."""
        return max(self, key=lambda z: z.x).x + 1

    def height(self) -> int:
        """Calculate the height of the map based on zone coordinates."""
        return max(self, key=lambda z: z.y).y + 1

    def add_zone(self, zone: Zone) -> None:
        if zone not in self.adj:
            self.adj[zone] = []

    def get_zone(self, name: str) -> Zone | None:
        return next((z for z in self if z.name == name), None)

    def add_connection(self, connection: Connection) -> None:
        self.add_zone(connection.a)
        self.add_zone(connection.b)
        self[connection.a].append(connection)
        self[connection.b].append(connection)
