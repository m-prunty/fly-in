#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    main.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/11 15:24:56 by maprunty         #+#    #+#              #
#    Updated: 2026/06/13 05:56:47 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
from display import TuiDisplay
from parser import Parser
from simulation import Simulation


def main():
    print("Hello from fly-in!")
    dm = Parser().parse_file("maps/easy/02_simple_fork.txt")
    sim = Simulation(drone_map=dm)
    disp = TuiDisplay(dm)
    disp.render(sim)


if __name__ == "__main__":
    main()
