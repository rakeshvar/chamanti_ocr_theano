#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import cairo
import pango
import pangocairo
import numpy as np

styles = '', ' Italic', ' Bold', ' Bold Italic'


def scribe(text, fontname, ten=10, style=0,
           sz=48, spc=1, movex=10, movey=0, twist=0):
    lines = text.split('\n')
    n_lines = len(lines)
    n_letters = max(len(line) for line in lines)

    size_x = 3 * ten * n_letters + 5 * ten
    size_y = 5 * ten * n_lines + 5 * ten

    # print("Lines: {} Letters:{} Size:{}x{}".format(
    #     n_lines, n_letters, size_x, size_y))

    data = np.zeros((size_y, size_x, 4), dtype=np.uint8)
    surf = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32,
                                              size_x, size_y)
    cr = cairo.Context(surf)
    pc = pangocairo.CairoContext(cr)
    pc.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

    layout = pc.create_layout()
    layout.set_text(text)

    style = styles[style]
    font_style = "{} {} {}".format(fontname, style, (sz * ten)//10)
    layout.set_font_description(pango.FontDescription(font_style))
    layout.set_spacing(spc * 32)

    cr.rectangle(0, 0, size_x, size_y)
    cr.set_source_rgb(1, 1, 1)
    cr.fill()
    cr.translate(ten, 0)
    cr.set_source_rgb(0, 0, 0)

    pc.update_layout(layout)
    pc.show_layout(layout)

    return data[:, :, 0] < 128
