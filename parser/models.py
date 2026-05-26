#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    models.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/25 01:27:37 by maprunty         #+#    #+#              #
#    Updated: 2026/05/25 12:30:43 by maprunty        ###   ########.fr        #
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
9Fly-in
Drones are interesting.
◦ normal – Standard zone with 1 turn movement cost (default)
◦ blocked – Inaccessible zone. Drones must not enter or pass through this zone.
Any path using it is invalid.
◦ restricted – A sensitive or dangerous zone. Movement to this zone costs 2
turns.
◦ priority – A preferred zone. Movement to this zone costs 1 turn but should
be prioritized in pathfinding.
"""

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum


class ZoneType(Enum):
    """Define type of a zone, which affects movement cost and accessibility."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


Meta = dict[str, ZoneType | str | int]


@dataclass(frozen=True)
class Zone:
    """Represent a zone in the drone map."""

    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1
    metadata: Meta = field(default_factory=dict)

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass(frozen=True)
class Connection:
    """Represent a connection between two zones, optional capacity."""

    a: Zone
    b: Zone
    max_link_capacity: int = 1
    metadata: Meta = field(default_factory=dict)


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

    def __iter__(self) -> Iterable[Zone]:
        return iter(self.adj)

    def add_zone(self, zone: Zone) -> None:
        if zone not in self.adj:
            self.adj[zone] = []

    def get_zone(self, name: str) -> Zone | None:
        print("get_zone", name)
        return next((z for z in self if z.name == name), None)

    def add_connection(self, connection: Connection) -> None:
        self.add_zone(connection.a)
        self.add_zone(connection.b)
        self[connection.a].append(connection)
        self[connection.b].append(connection)
