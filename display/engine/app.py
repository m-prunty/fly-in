#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    app.py                                            :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/27 19:48:04 by maprunty         #+#    #+#              #
#    Updated: 2026/05/28 01:23:52 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from .mlx import Mlx


class App:
    def __init__(self):
        self.name = "My App"
        mlx = Mlx()
        self.mlx_ptr = mlx.mlx_init()

    def run(self):
        print(f"Running {self.name}...")
