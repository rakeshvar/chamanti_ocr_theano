#! /usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Uses cffi_wrapper to render given text to image.
'''
import random
import array

import numpy as np

import cffi_wrapper as cp
import cairocffi
from trimmers import horztrim


def scribe(text, font_style,
           width, height,
           movex, movey,
           twist):

    fmt = cairocffi.FORMAT_A8
    width = cairocffi.ImageSurface.format_stride_for_width(fmt, width)
    data = array.array('b', [0] * (height * width))
    surface = cairocffi.ImageSurface(fmt, width, height, data, width)
    context = cairocffi.Context(surface)
    # cffi.pangocairo.pango_cairo_set_antialias(cffi.cairo.ANTIALIAS_SUBPIXEL)
    context.translate(movex, movey)
    context.rotate(twist)

    layout = cp.gobject_ref(cp.pangocairo.pango_cairo_create_layout(context._pointer))
    cp.pango.pango_layout_set_text(layout, text.encode('utf8'), -1)

    font_desc = cp.pango.pango_font_description_from_string(font_style.encode('utf8'))
    cp.pango.pango_layout_set_font_description(layout, font_desc)
    # pango.pango_layout_set_spacing(spc * 32)

    cp.pangocairo.pango_cairo_update_layout(context._pointer, layout)
    cp.pangocairo.pango_cairo_show_layout(context._pointer, layout)

    # print(surface.get_width(), surface.get_height())

    return np.frombuffer(data, dtype=np.uint8).reshape((height, width))


def scribe_wrapper(text, fontname, styleid, size,
                   height, hbuffer, vbuffer,
                   twist):
    styles = '', ' Italic', ' Bold', ' Bold Italic'
    font_style = "{} {} {}".format(fontname, styles[styleid], size)

    lines = text.split('\n')
    n_lines = len(lines)
    n_letters = max(len(line) for line in lines)
    line_ht = height / (n_lines+1)
    letter_wd = .7 * line_ht
    width = round((n_letters+2) * letter_wd)

    return scribe(text, font_style, width, height, hbuffer, vbuffer, twist)


class Scribe():
    def __init__(self, language, **kwargs):
        self.language = language
        self.height = kwargs["height"]
        self.vbuffer = kwargs["vbuffer"]
        self.hbuffer = kwargs["hbuffer"]
        self.maxangle = kwargs["maxangle"]
        self.nchars = kwargs["nchars_per_sample"]
        self.size = kwargs["size"]
        self.noise = kwargs["noise"]

    def __call__(self):
        twist = self.maxangle * random.uniform(-1, 1)
        fontname, rel_size, styleid = self.language.random_font()

        text = self.language.get_word(self.nchars)
        img = scribe_wrapper(text, fontname, styleid, self.size,
                             self.height, self.hbuffer, self.vbuffer, twist)

        img = horztrim(img, self.hbuffer)

        return img, self.language.get_labels(text)

    def __str__(self):
        return "Height:{} Buffers:v{} h{} Size:{}" \
               "\nAngle:{:.2f} Noise:{:.2f}" \
               "\nNumChars:{}".format(
            self.height, self.vbuffer, self.hbuffer, self.size,
            self.maxangle, self.noise, self.nchars
        )