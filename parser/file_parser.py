#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    file_parser.py                                    :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/25 01:15:56 by maprunty         #+#    #+#              #
#    Updated: 2026/06/13 05:35:33 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Tokenises lines, validates syntax, raises ParseError.

nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: roof2 6 2 [zone=normal color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [zone=normal color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]
connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal

The first line defines the number of drones using nb_drones:
<number>.
• Zone definition on each line using type prefixes:
◦ start_hub:
◦ end_hub:
◦ hub:
<name> <x> <y> [metadata] marks the starting zone.
<name> <x> <y> [metadata] marks the end zone.
<name> <x> <y> [metadata] defines a regular zone.
◦ The connection syntax forbids dashes in zone names (see below).
• All metadata is optional and enclosed in brackets [...] with default values:
◦ zone=<type> (default: normal)
◦ color=<value> (default: none)
◦ max_drones=<number> (default: 1) - Maximum drones that can occupy this
zone simultaneously
◦ Tags inside brackets can appear in any order.
"""

from collections.abc import Iterator

from domain import Connection, DroneMap, MetaData, Vec2, Zone


class ParseError(Exception):
    """Custom exception for parsing errors."""

    def __init__(self, message: str):
        super().__init__(message)


class Parser:
    def __init__(self) -> None:
        self._line: str | None = None
        self._line_num = 0
        self.drone_map: DroneMap | None = None

    def parse_file(self, file_path: str) -> DroneMap:
        """Parse the input file and return a DroneMap object."""
        parse_dict: dict[str, list[str]] = {
            "start_hub": [],
            "end_hub": [],
            "hub": [],
            "connection": [],
        }
        with open(file_path) as f:
            lines = self._yd_line(f.readlines())
        line = next(lines)
        nb_drones = int(line[1]) if line[0] == "nb_drones" else None
        if nb_drones is None:
            raise ParseError(f"First line must define nb_drones: {line}")
        for line in lines:
            if line[0] in parse_dict:
                parse_dict[line[0]].append(line[1])
            else:
                raise ParseError(
                    f"Unknown line type: {line[0]} at line {self._line_num}"
                )
        if (
            len(parse_dict["start_hub"]) != 1
            or len(parse_dict["end_hub"]) != 1
        ):
            raise ParseError(
                "There must be exactly one start_hub and one end_hub"
            )
        start_zone = self._parse_zone(parse_dict["start_hub"][0])
        end_zone = self._parse_zone(parse_dict["end_hub"][0])
        self.drone_map = DroneMap(
            nb_drones=nb_drones, start_zone=start_zone, end_zone=end_zone
        )
        self.drone_map.add_zone(start_zone)
        self.drone_map.add_zone(end_zone)
        self._add_zones(parse_dict["hub"])
        self._add_connections(parse_dict["connection"])
        return self.drone_map

    def _yd_line(self, lines: list[str]) -> Iterator[list[str]]:
        for line in lines:
            self._line_num += 1
            if line.strip() != "" and not line.strip().startswith("#"):
                yield line.strip().split(":")

    def _parse_zone(self, line: str) -> Zone:
        zone, x, y, *meta = line.split()
        metadata = self._parse_metadata(meta)
        return Zone(name=zone, loc=Vec2(int(x), int(y)), **metadata)

    def _add_zones(self, lines: list[str]) -> None:
        assert self.drone_map is not None
        for line in lines:
            self.drone_map.add_zone(self._parse_zone(line))

    def _parse_connection(self, line: str) -> Connection:
        connection, *meta = line.split()
        if "-" not in connection:
            raise ParseError(f"Invalid connection format: {line}")
        a_name, b_name = connection.split("-", 1)
        metadata = self._parse_metadata(meta)
        assert self.drone_map
        a = self.drone_map.get_zone(a_name)
        b = self.drone_map.get_zone(b_name)
        assert a is not None and b is not None, (
            f"Connection references undefined zones: {a_name}, {b_name}"
        )
        return Connection(
            a=a,
            b=b,
        )

    def _add_connections(self, lines: list[str]) -> None:
        assert self.drone_map is not None
        for line in lines:
            print("Adding connection:", line)
            self.drone_map.add_connection(self._parse_connection(line))

    def _parse_metadata(self, metadata_str: list[str]) -> MetaData:
        if not metadata_str:
            return MetaData()
        meta_str = " ".join(metadata_str)
        if not (meta_str.startswith("[") and meta_str.endswith("]")):
            raise ParseError(f"Invalid metadata format: {meta_str}")
        meta_str = meta_str[1:-1].strip()
        return MetaData(item.split("=", 1) for item in meta_str.split())
