#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import array
import numpy as np
import cffi_wrapper as cffi

styles = '', ' Italic', ' Bold', ' Bold Italic'
# TODO: Make scribe a class


def scribe(text, fontname, ten=10, style=0,
           size=48, spacing=1, movex=10, movey=0, twist=0):
    lines = text.split('\n')
    n_lines = len(lines)
    n_letters = max(len(line) for line in lines)
    size_x = 3 * ten * n_letters + 5 * ten
    size_y = 5 * ten * n_lines + 5 * ten
    fmt = cffi.cairocffi.FORMAT_A8
    dtype = np.uint8
    arrtype = 'b'

    size_x = cffi.cairocffi.ImageSurface.format_stride_for_width(fmt, size_x)
    data = array.array(arrtype, [0] * (size_y * size_x))
    surface = cffi.cairocffi.ImageSurface(fmt, size_x, size_y, data, size_x)
    context = cffi.cairocffi.Context(surface)
    # pangocairo.pango_cairo_set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    context.translate(movex, movey)
    context.rotate(twist)

    layout = cffi.gobject_ref(cffi.pangocairo.pango_cairo_create_layout(context._pointer))
    cffi.pango.pango_layout_set_text(layout, text.encode('utf8'), -1)

    style = styles[style]
    font_style = "{} {} {}".format(fontname, style, (size * ten) // 10)
    font_desc = cffi.pango.pango_font_description_from_string(font_style.encode('utf8'))
    cffi.pango.pango_layout_set_font_description(layout, font_desc)
    # pango.pango_layout_set_spacing(spc * 32)

    cffi.pangocairo.pango_cairo_update_layout(context._pointer, layout)
    cffi.pangocairo.pango_cairo_show_layout(context._pointer, layout)

    # print(surface.get_width(), surface.get_height())

    return np.frombuffer(data, dtype=dtype).reshape((size_y, size_x))


def trim(nparr):
    good_rows = np.where(np.sum(nparr, axis=1) > 0)[0]
    good_cols = np.where(np.sum(nparr, axis=0) > 0)[0]

    try:
        return nparr[good_rows.min():good_rows.max() + 1,
                     good_cols.min():good_cols.max() + 1]
    except ValueError:
        return np.array([[]])


def smartrim(nparr, target_ht, wd_buffer):
    ht, wd = nparr.shape
    assert ht >= target_ht

    good_rows = np.where(np.sum(nparr, axis=1) > 0)[0]
    good_cols = np.where(np.sum(nparr, axis=0) > 0)[0]

    if len(good_rows):
        top, bot = good_rows.min(), good_rows.max() + 1
        lft, rgt = good_cols.min(), good_cols.max() + 1
    else:
        top, bot, lft, rgt = 0, target_ht, wd_buffer, wd_buffer + 1

    ######## Center and Clip
    newtop = max(0, top + (bot - top - target_ht) // 2)
    newbot = newtop + target_ht
    if newbot > ht:
        print('Ht {}, top{}, bot{}, newtop{}, newbot{}'.format(ht, top, bot,
                                                               newtop, newbot))
        newbot = ht
        newtop = newbot - target_ht

    assert newbot - newtop == target_ht

    ######## Buffer
    lft = max(0, lft - wd_buffer)
    rgt = min(rgt + wd_buffer, wd)

    return nparr[newtop:newbot, lft:rgt]