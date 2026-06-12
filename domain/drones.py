#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    drones.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/27 18:03:21 by maprunty         #+#    #+#              #
#    Updated: 2026/05/27 19:39:26 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from dataclasses import dataclass, field
from enum import Enum

from .models import Meta
from .vector import Vec2


class DroneState(Enum):
    """Define the state of a drone in the simulation."""

    IDLE = "idle"
    MOVING = "moving"
    DELIVERED = "delivered"
    WAITING = "waiting"


@dataclass
class Drone:
    """Represents a drone in the simulation."""

    id: str
    position: Vec2
    state: DroneState = DroneState.IDLE
    metadata: Meta = field(default_factory=dict)
