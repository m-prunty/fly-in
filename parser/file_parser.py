#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    file_parser.py                                    :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/25 01:15:56 by maprunty         #+#    #+#              #
#    Updated: 2026/05/25 16:17:55 by maprunty        ###   ########.fr        #
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

from .models import Connection, DroneMap, Meta, Zone


class ParseError(Exception):
    """Custom exception for parsing errors."""

    def __init__(self, message: str):
        super().__init__(message)


class Parser:
    """Parser for the drone map input file.

    VII.4
    Parser Constraints
    The input file must respect the expected structure and syntax:
    • The first line must define the number of drones using nb_drones:
    <positive_integer>.
    • The program must be able to handle any number of drones.
    • There must be exactly one start_hub: zone and one end_hub: zone.
    • Each zone must have a unique name and valid integer coordinates.
    • Zone names can use any valid characters but dashes and spaces.
    • Connections must link only previously defined zones using connection:
    [metadata].
    <zone1>-<zone2>
    • The same connection must not appear more than once (e.g., a-b and b-a are con-
    sidered duplicates).
    • Any metadata block (e.g., [zone=... color=...] for zones, [max_link_capacity=...]
    for connections) must be syntactically valid.
    • Zone types must be one of: normal, blocked, restricted, priority. Any invalid
    type must raise a parsing error.
    • Capacity values (max_drones for zones, max_link_capacity for connections) must
    be positive integers.
    • Any other parsing error must stop the program and return a clear error message
    indicating the line and cause.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.line: str | None = None
        self.line_num = 0
        self._drone_map: DroneMap | None = None

    def parse_file(self) -> DroneMap:
        """Parse the input file and return a DroneMap object."""
        parse_dict: dict[str, list[str]] = {
            "start_hub": [],
            "end_hub": [],
            "hub": [],
            "connection": [],
        }
        with open(self.file_path) as f:
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
                    f"Unknown line type: {line[0]} at line {self.line_num}"
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
        self._drone_map = DroneMap(
            nb_drones=nb_drones, start_zone=start_zone, end_zone=end_zone
        )
        self._add_zones(parse_dict["hub"])
        self._add_connections(parse_dict["connection"])
        return self._drone_map

    def _yd_line(self, lines: str) -> Iterator[list[str]]:
        for line in lines:
            self.line_num += 1
            if line.strip() != "" and not line.strip().startswith("#"):
                yield line.strip().split(":")

    def _parse_zone(self, line: str) -> Zone:
        zone, x, y, *meta = line.split()
        metadata = self._parse_metadata(meta)
        return Zone(name=zone, x=int(x), y=int(y), metadata=metadata)

    def _add_zones(self, lines: list[str]) -> None:
        assert self._drone_map is not None
        for line in lines:
            self._drone_map.add_zone(self._parse_zone(line))

    def _parse_connection(self, line: str) -> Connection:
        connection, *meta = line.split()
        if "-" not in connection:
            raise ParseError(f"Invalid connection format: {line}")
        a_name, b_name = connection.split("-", 1)
        metadata = self._parse_metadata(meta)
        assert self._drone_map
        return Connection(
            a=self._drone_map.get_zone(a_name),
            b=self._drone_map.get_zone(b_name),
            metadata=metadata,
        )

    def _add_connections(self, lines: list[str]) -> None:
        assert self._drone_map is not None
        for line in lines:
            print("Adding connection:", line)
            self._drone_map.add_connection(self._parse_connection(line))

    def _parse_metadata(self, metadata_str: list[str]) -> Meta:
        metadata = {}
        if not metadata_str:
            return metadata
        meta_str = " ".join(metadata_str)
        if not (meta_str.startswith("[") and meta_str.endswith("]")):
            raise ParseError(f"Invalid metadata format: {meta_str}")
        meta_str = meta_str[1:-1].strip()
        return dict(item.split("=", 1) for item in meta_str.split())
