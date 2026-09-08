#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    mlx_display.py                                    :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/05/27 19:48:04 by maprunty         #+#    #+#              #
#    Updated: 2026/09/08 06:04:18 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import sys
from dataclasses import dataclass

from mlx import Mlx

from .base_display import Display

RGB: dict[str, tuple[int, int, int]] = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 200, 0),
    "yellow": (230, 200, 0),
    "blue": (0, 90, 220),
    "magenta": (200, 0, 200),
    "cyan": (0, 200, 200),
    "white": (255, 255, 255),
}


@dataclass
class ImgData:
    """Structure for image data"""

    img = None
    width: int = 0
    height: int = 0
    data = None
    sl: int = 0  # size line
    bpp: int = 0  # bits per pixel
    iformat: int = 0


@dataclass
class XVar:
    """Structure for main vars"""

    mlx: Mlx | None = None
    mlx_ptr: None = None
    screen_w: int = 0
    screen_h: int = 0
    win_ptr = None
    win_2 = None
    img_1 = ImgData()
    img_2 = ImgData()
    img_png = ImgData()
    img_xpm = ImgData()
    imgidx: int = 0


class MlxDisplay(Display):
    def __init__(self, drone_map):
        super().__init__(drone_map)
        self.name = "Mlx Fly-In"
        self.cell_size = 20
        self.scale = 1

        #       frame = self.build()
        #       frame_height = len(frame)
        #       frame_width = max(len(row) for row in frame) if frame else 0
        #
        #       print(f"Frame dimensions: {frame_width}x{frame_height}")
        #       self.width_win = frame_width * self.cell_size * self.scale
        #       self.height_win = frame_height * self.cell_size * self.scale
        #       print(f"Window dimensions: {self.width_win}x{self.height_win}")

        self.mlx_setup()
        self.mlx_create_windows()
        self.mlx_create_images()
        self.mlx_fill_images()
        self._rendered = False

    def mlx_setup(self):
        self.xvar = XVar()
        # Mlx Initialisation
        try:
            self.xvar.mlx = Mlx()
            self.xvar.mlx_ptr = self.xvar.mlx.mlx_init()
            ret, self.xvar.screen_w, self.xvar.screen_h = (
                self.xvar.mlx.mlx_get_screen_size(self.xvar.mlx_ptr)
            )
        except Exception as e:
            print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"Screen size: {self.xvar.screen_w} x {self.xvar.screen_h}")

    def mlx_create_windows(self):
        # Windows creation
        try:
            self.xvar.win_ptr = self.xvar.mlx.mlx_new_window(
                self.xvar.mlx_ptr, 400, 400, "MLX main win"
            )
            if not self.xvar.win_ptr:
                raise Exception("Can't create main window")

            self.xvar.win_2 = self.xvar.mlx.mlx_new_window(
                self.xvar.mlx_ptr, 150, 150, "Secondary window"
            )
            if not self.xvar.win_2:
                raise Exception("Can't create secondary window")
        except Exception as e:
            print(f"Error Win create: {e}", file=sys.stderr)
            sys.exit(1)

    def mlx_create_images(self):
        # Image #1
        self.xvar.img_1.img = self.xvar.mlx.mlx_new_image(
            self.xvar.mlx_ptr, 200, 200
        )
        if not self.xvar.img_1.img:
            raise Exception("Can't create image 1")

        self.xvar.img_1.width = 200
        self.xvar.img_1.height = 200
        (
            self.xvar.img_1.data,
            self.xvar.img_1.bpp,
            self.xvar.img_1.sl,
            self.xvar.img_1.iformat,
        ) = self.xvar.mlx.mlx_get_data_addr(self.xvar.img_1.img)

    def mlx_fill_images(self):
        # Fill image #1
        for i in range(self.xvar.img_1.sl * 200):
            self.xvar.img_1.data[i] = 0x80
        for i in range(self.xvar.img_1.sl * 100):
            self.xvar.img_1.data[i] = 0xFF

        try:
            # Add some red pixels
            pixel_positions = [
                0 * 200 * 4,  # top left
                (1 * 200 + 1) * 4,  # top left + 1
                (199 * 200 + 199) * 4,  # bottom right
                (198 * 200 + 198) * 4,  # bottom right - 1
                100 * 200 * 4,  # middle left
                (100 * 200 + 100) * 4,  # middle
                100 * 200 * 4 + 199 * 4,  # middle right
                50 * 200 * 4 + 50 * 4,  # quarter
                150 * 200 * 4 + 150 * 4,  # three quarters
            ]
            for pos in pixel_positions:
                if pos < len(self.xvar.img_1.data) - 3:
                    self.xvar.img_1.data[pos : pos + 4] = (
                        0xFFFF0000
                    ).to_bytes(4, "little")
        except Exception as e:
            print(f"Error img1: {e}", file=sys.stderr)
            sys.exit(1)

    def run(self):
        print(f"Running {self.name}...")
        # self.xvar.mlx.mlx_loop_hook(self.xvar.mlx_ptr, self._on_loop, None)
        self.xvar.mlx.mlx_put_image_to_window(
            self.xvar.mlx_ptr, self.xvar.win_ptr, self.xvar.img_1.img, 100, 100
        )
        self.xvar.mlx.mlx_loop(self.xvar.mlx_ptr)

    def render(self):
        print(f"Rendering {self.name}...")
        frame = self.build()
        for y, row in enumerate(frame):
            for x, entry in enumerate(row):
                color_name = self._color_for(entry)
                print(color_name, end=" ")
                if color_name is None:
                    continue
                color = RGB[color_name]
                self._draw_cell(
                    x * self.cell_size * self.scale,
                    y * self.cell_size * self.scale,
                    color,
                )

    def _on_loop(self, param):
        if not self._rendered:
            self.render()
            self._rendered = True
        return 0

    #    def mlx_setup(self):
    #        self.mlx_ptr = self.m.mlx_init()
    #        self.win_ptr = self.m.mlx_new_window(
    #            self.mlx_ptr, self.width_win, self.height_win, self.name
    #        )
    #        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
    #        (ret, w, h) = self.m.mlx_get_screen_size(self.mlx_ptr)
    #        print(f"Got screen size: {w} x {h} , {ret}.")
    #
    #        self.m.mlx_mouse_hook(self.win_ptr, self.mymouse, None)
    #        self.m.mlx_key_hook(self.win_ptr, self.mykey, None)
    #        self.m.mlx_hook(self.win_ptr, 33, 0, self.gere_close, None)
    #
    #
    #    def mymouse(self, button, x, y, mystuff):
    #        print(f"Got mouse event! button {button} at {x},{y}.")
    #
    #    def mykey(self, keynum, mystuff):
    #        print(f"Got key {keynum}, and got my stuff back:")
    #        print(mystuff)
    #        if keynum == 32:
    #            self.m.mlx_mouse_hook(self.win_ptr, None, None)
    #
    #    def gere_close(self, dummy):
    #        print(">>>>>>>", dummy)
    #        self.m.mlx_loop_exit(self.mlx_ptr)
    #        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
    #
    def _draw_cell(self, x, y, color):
        """Draw a cell at (x, y) with the given color."""
        color_int = self.rgb_to_int(color)
        print(">>>>", hex(color_int))
        self.xvar.mlx.mlx_pixel_put(
            self.xvar.mlx_ptr, self.xvar.win_ptr, 4, 4, 0xFF0000
        )
        for i in range(self.cell_size * self.scale):
            for j in range(self.cell_size * self.scale):
                print(
                    f"Drawing pixel at ({x + i}, {y + j}) with color {color_int}"
                )
                self.xvar.mlx.mlx_pixel_put(
                    self.xvar.mlx_ptr, self.xvar.win_ptr, x + i, y + j, 255
                )

    def rgb_to_int(self, rgb: tuple[int, int, int]) -> int:
        r, g, b = rgb
        return (r << 16) | (g << 8) | b
