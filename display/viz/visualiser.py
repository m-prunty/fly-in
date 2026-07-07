#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    visualiser.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/28 01:48:24 by maprunty         #+#    #+#              #
#    Updated: 2026/05/28 01:48:32 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class MovementToken:
    # e.g. "D1-roof1" or "D2-tunnelB->roofX" depending on your final format
    text: str


class Visualizer(Protocol):
    def on_sim_start(self) -> None: ...
    def on_turn_start(self, turn: int) -> None: ...
    def on_turn_end(
        self, turn: int, moves: Sequence[MovementToken]
    ) -> None: ...
    def on_sim_end(self, turns: int) -> None: ...
