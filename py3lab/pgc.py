#!/usr/bin/env python3
from gi.repository import Pango, PangoCairo
import cairo

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 120, 120)
context = cairo.Context(surf)
pgc = PangoCairo.create_context(context)
layout = Pango.Layout(context)
layout.set_text("ABC")
font = Pango.FontDescription('/home/rakesha/.fonts/Mallanna.ttf')