#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import cairo
import pango
import pangocairo

import numpy as np
from telugu_fonts import font_properties

all_chars = (u' ఁంఃఅఆఇఈఉఊఋఌఎఏఐఒఓఔ'
             u'కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమ'
             u'యరఱలళవశషసహ'
             u'ఽాిీుూృౄెేైొోౌ్'
             u'ౘౙౠౡౢౣ'
             u'౦౧౨౩౪౫౬౭౮౯')


def tel2int(text):
    return [all_chars.find(char)+1 for char in text]


def pprint(nparr):
    print('-' * (len(nparr[0]) + 5))
    for ir, r in enumerate(nparr):
        print('{:3d}|'.format(ir), end='')
        for p in r:
            print([' ', '#'][1 * p], end='')
        print('|')
    print('-' * (len(nparr[0]) + 5))


style_ids = {'': '_NR', ' Bold': '_BL', ' Italic': '_IT', ' Bold Italic': '_BI'}


def scribe(text, fontname, ten=10, style=''):
    lines = text.split('\n')
    n_lines = len(lines)
    n_letters = max(len(line) for line in lines)

    size_x = 3 * ten * n_letters + 5 * ten  # TODO: Take into account # of spaces
    size_y = 5 * ten * n_lines + 5 * ten
    # print("Lines: ", n_lines)
    # print("Letters: ", n_letters)
    # print("Size X: ", size_x)
    # print("Size Y: ", size_y)

    data = np.zeros((size_y, size_x, 4), dtype=np.uint8)
    surf = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32,
                                              size_x, size_y)
    cr = cairo.Context(surf)
    pc = pangocairo.CairoContext(cr)
    pc.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

    layout = pc.create_layout()
    layout.set_text(text)

    [sz, gho, rep, ppu, spc, abbr, hasbold] = font_properties[fontname]

    fontname += ',' + style + ' ' + str(sz * ten / 10)
    layout.set_font_description(pango.FontDescription(fontname))
    layout.set_spacing(spc * 32)

    cr.rectangle(0, 0, size_x, size_y)
    cr.set_source_rgb(1, 1, 1)
    cr.fill()
    cr.translate(ten, 0)
    cr.set_source_rgb(0, 0, 0)

    pc.update_layout(layout)
    pc.show_layout(layout)

    return data[:, :, 0] < 128


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
    if len(sys.argv) < 2:
        print("Usage:\n"
              "{0} text_file"
              "\n or \n"
              "{0} <(echo 'text')".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as fin:
        print("Opening ", sys.argv[1])
        txt = fin.read().decode('utf8')

    try:
        tenn = int(sys.argv[2])
    except IndexError:
        tenn = 10

    for font in sorted(font_properties):
        x = scribe(txt, font, tenn)
        pprint(x)
        pprint(trim(x))
        # break
