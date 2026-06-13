#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    drones.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/27 18:03:21 by maprunty         #+#    #+#              #
#    Updated: 2026/06/13 05:06:33 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from dataclasses import dataclass
from enum import Enum

from .models import Transit, Zone


class DroneState(Enum):
    """Define the state of a drone in the simulation."""

    IDLE = "idle"
    MOVING = "moving"
    DELIVERED = "delivered"
    WAITING = "waiting"


@dataclass
class Drone:
    """Represent a drone in the simulation."""

    id: int
    location: Zone
    transit: Transit | None = None
    status: DroneState = DroneState.IDLE
