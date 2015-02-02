#!/usr/bin/env python3

from gi.repository import Gtk, Gdk, cairo, Pango, PangoCairo
import math
import sys


RADIUS = 150
N_WORDS = 10
FONT = "Sans Bold 12"


class Squareset(Gtk.DrawingArea):
    def __init__ (self, upper=9, text=''):
##        Gtk.Widget.__init__(self)
        Gtk.DrawingArea.__init__(self)
        self.set_size_request (200, 200)
##        self.show_all()

    def do_draw_cb(self, widget, cr):
        # The do_draw_cb is called when the widget is asked to draw itself
        # with the 'draw' as opposed to old function 'expose event'
        # Remember that this will be called a lot of times, so it's usually
        # a good idea to write this code as optimized as it can be, don't
        # Create any resources in here.

        cr.translate ( RADIUS, RADIUS)

        layout = PangoCairo.create_layout (cr)
        layout.set_text("శ్రీమదాంధ్రమహాభారతము", -1)
        desc = Pango.font_description_from_string (FONT)
        layout.set_font_description( desc)

        rangec = range(0, N_WORDS)
        for i in rangec:
            width, height = 0,0
            angle = (360. * i) / N_WORDS;

            cr.save ()

            red   = (1 + math.cos ((angle - 60) * math.pi / 180.)) / 2
            cr.set_source_rgb ( red, 0, 1.0 - red)
            cr.rotate ( angle * math.pi / 180.)
            #/* Inform Pango to re-layout the text with the new transformation */
            PangoCairo.update_layout (cr, layout)
            width, height = layout.get_size()
            cr.move_to ( - (float(width) / 1024.) / 2, - RADIUS)
            PangoCairo.show_layout (cr, layout)
            cr.restore()


def destroy(window):
        Gtk.main_quit()


def main():
    window = Gtk.Window()
    window.set_title ("Hello World")

    app = Squareset()

    window.add(app)

    app.connect('draw', app.do_draw_cb)
    window.connect_after('destroy', destroy)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())