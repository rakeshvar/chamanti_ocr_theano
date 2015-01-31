#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Pango, PangoCairo
#import cairo
import cairocffi as cairo

surface = cairo.ImageSurface(cairo.FORMAT_A8, 120, 120)
context = cairo.Context(surface)
layout = PangoCairo.create_layout(context)
layout.set_text("ర్మణ్యే", -1)
font_desc = Pango.FontDescription('/home/rakesha/.fonts/Ponnala.ttf 32')
layout.set_font_description(font_desc)
PangoCairo.update_layout(context, layout)
PangoCairo.show_layout(context, layout)

########################################## Save to File
with open("blah.png", "wb") as img_f:
    surface.write_to_png(img_f)

########################################## Save to Text
import io
b = io.BytesIO()
surface.write_to_png(b)
b.seek(0)

########################################## Open from Text
from PIL import Image as im
import numpy
img = im.open(b)

a = numpy.array(img)
print(a.shape)

def pprint(a):
    for r in a:
        for c in r:
            if c == 0 : v=' '
            elif c < .2: v = '.'
            elif c < .4: v = '*'
            elif c < .6: v = 'o'
            elif c < .8: v = '0'
            elif c < 1:  v = '@'
            else:  v = '#'
            print(v, end='')
        print()

pprint(a/255)