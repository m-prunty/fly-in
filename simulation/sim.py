#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    sim.py                                            :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/13 05:19:20 by maprunty         #+#    #+#              #
#    Updated: 2026/06/13 05:20:18 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


from dataclasses import dataclass, field

from domain import Drone, DroneMap, Zone


@dataclass(frozen=True)
class MoveEvent:
    tick: int
    drone: Drone
    from_zone: Zone
    to_zone: Zone


@dataclass
class Simulation:
    drone_map: DroneMap
    tick: int = 0
    history: list[MoveEvent] = field(default_factory=list)
    drones: list[Drone] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.drones = [
            Drone(id=i, location=self.drone_map.start_zone)
            for i in range(self.drone_map.nb_drones)
        ]

    def step(self):
        print("Stepping simulation...")
        # for drone in self.drones:
        #    if drone.state == DroneState.MOVING:
