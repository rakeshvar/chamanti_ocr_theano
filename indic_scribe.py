#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from cffi_wrapper import *
import numpy as np
import array

styles = '', ' Italic', ' Bold', ' Bold Italic'
# TODO: Make scribe a class


def scribe(text, fontname, ten=10, style=0,
           size=48, spacing=1, movex=10, movey=0, twist=0):
    lines = text.split('\n')
    n_lines = len(lines)
    n_letters = max(len(line) for line in lines)

    # TODO: Take into account # of spaces
    size_x = 3 * ten * n_letters + 5 * ten
    size_y = 5 * ten * n_lines + 5 * ten

    # print("Lines: {} Letters:{} Size:{}x{}".format(
    #     n_lines, n_letters, size_x, size_y))

    ####### CFFI Code
    fmt, dtype, arrtype = cairocffi.FORMAT_A8, np.uint8, 'b'

    size_x = cairocffi.ImageSurface.format_stride_for_width(fmt, size_x)
    data = array.array(arrtype, [0] * (size_y * size_x))
    surface = cairocffi.ImageSurface(fmt, size_x, size_y, data, size_x)

    context = cairocffi.Context(surface)
    # pangocairo.pango_cairo_set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    context.translate(movex, movey)
    context.rotate(twist)

    layout = gobject_ref(pangocairo.pango_cairo_create_layout(context._pointer))
    pango.pango_layout_set_text(layout, text.encode('utf8'), -1)

    style = styles[style]
    font_style = "{} {} {}".format(fontname, style, (size * ten)//10)
    font_desc = pango.pango_font_description_from_string(
        font_style.encode('utf8'))
    pango.pango_layout_set_font_description(layout, font_desc)
    # pango.pango_layout_set_spacing(spc * 32)
    # cr.rectangle(0, 0, size_x, size_y)
    # cr.set_source_rgb(1, 1, 1)
    # cr.fill()
    # cr.translate(ten, 0)
    # cr.set_source_rgb(0, 0, 0)

    pangocairo.pango_cairo_update_layout(context._pointer, layout)
    pangocairo.pango_cairo_show_layout(context._pointer, layout)

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
        top, bot, lft, rgt = 0, target_ht, wd_buffer, wd_buffer+1

    ######## Center and Clip
    newtop = max(0, top + (bot - top - target_ht)//2)
    newbot = newtop + target_ht
    if newbot > ht:
        print('Ht {}, top{}, bot{}, newtop{}, newbot{}'.format(ht, top, bot,
                                                               newtop, newbot))
        newbot = ht
        newtop = newbot - target_ht

    assert newbot-newtop == target_ht

    ######## Buffer
    lft = max(0, lft-wd_buffer)
    rgt = min(rgt+wd_buffer, wd)

    return nparr[newtop:newbot, lft:rgt]


if __name__ == '__main__':
    import sys
    from telugu_fonts import font_properties
    from print_utils import pprint

    if len(sys.argv) < 2:
        print("Usage:\n"
              "{0} text_file"
              "\n or \n"
              "{0} <(echo 'text')".format(sys.argv[0]))
        sys.exit()

    corpus_file = sys.argv[1]
    with open(corpus_file) as fin:
        print("Opening ", corpus_file)
        txt = fin.read()

    try:
        tenn = int(sys.argv[2])
    except IndexError:
        tenn = 10

    for font in sorted(font_properties):
        x = scribe(txt, font, tenn)
        pprint(x)
        pprint(smartrim(x, tenn*3, tenn//2))