#!/usr/bin/python3
# coding: utf8
import array
import cairocffi
import cffi


ffi = cffi.FFI()
ffi.include(cairocffi.ffi)
ffi.cdef('''
    /* GLib */
    typedef void* gpointer;
    void g_object_unref (gpointer object);

    /* Pango and PangoCairo */
    typedef ... PangoLayout;
    typedef enum {
        PANGO_ALIGN_LEFT,
        PANGO_ALIGN_CENTER,
        PANGO_ALIGN_RIGHT
    } PangoAlignment;
    int pango_units_from_double (double d);
    PangoLayout * pango_cairo_create_layout (cairo_t *cr);
    void pango_cairo_show_layout (cairo_t *cr, PangoLayout *layout);
    void pango_cairo_update_layout (cairo_t *cr, PangoLayout *layout);
    void pango_layout_set_width (PangoLayout *layout, int width);
    void pango_layout_set_alignment (
        PangoLayout *layout, PangoAlignment alignment);
    void pango_layout_set_markup (
        PangoLayout *layout, const char *text, int length);
    void pango_layout_set_text (
        PangoLayout *layout, const char *text, int length);

    typedef ... PangoFontDescription;
    PangoFontDescription*
        pango_font_description_new(void);
    void
        pango_font_description_set_family(
            PangoFontDescription *desc, const char *family);
    void
        pango_layout_set_font_description(
            PangoLayout *layout, const PangoFontDescription *desc);
    PangoFontDescription *
        pango_font_description_from_string (const char *str);
    void
        pango_font_description_set_size (
            PangoFontDescription *desc, int size);
''')
gobject = ffi.dlopen('gobject-2.0')
pango = ffi.dlopen('pango-1.0')
pangocairo = ffi.dlopen('pangocairo-1.0')

gobject_ref = lambda pointer: ffi.gc(pointer, gobject.g_object_unref)
units_from_double = pango.pango_units_from_double

# ####################
import numpy as np


def get_numpy(text="స్కారం", ht=30, wd=70, size=20, font="LakkiReddy"):
    fmt, dtype, arrtype = cairocffi.FORMAT_A8, np.uint8, 'b'

    wd = cairocffi.ImageSurface.format_stride_for_width(fmt, wd)
    data = array.array(arrtype, [0] * (ht * wd))
    surface = cairocffi.ImageSurface(fmt, wd, ht, data, wd)

    context = cairocffi.Context(surface)
    context.translate(0, 0)  #x, y
    context.rotate(-0.1)

    layout = gobject_ref(pangocairo.pango_cairo_create_layout(context._pointer))
    pango.pango_layout_set_text(layout, text.encode('utf8'), -1)
    font = "{} {}".format(font, size)
    font_desc = pango.pango_font_description_from_string(font.encode('utf8'))
    pango.pango_layout_set_font_description(layout, font_desc)
    pangocairo.pango_cairo_update_layout(context._pointer, layout)
    pangocairo.pango_cairo_show_layout(context._pointer, layout)

    print(surface.get_width(), surface.get_height())

    return np.frombuffer(data, dtype=dtype).reshape((ht, wd))


def slab_print(slab):
    """
    Prints a 'slab' of printed 'text' using ascii.
    :param slab: A matrix of floats from [0, 1]
    """
    for ir, r in enumerate(slab):
        print('{:2d}¦'.format(ir), end='')
        for val in r:
            if val < 0.0:
                print('-', end='')
            elif val < .15:
                print(' ', end=''),
            elif val < .35:
                print('░', end=''),
            elif val < .65:
                print('▒', end=''),
            elif val < .85:
                print('▓', end=''),
            elif val <= 1.:
                print('█', end=''),
            else:
                print('+', end='')
        print('¦')


if __name__ == '__main__':
    rendered = get_numpy()
    print(rendered.max(), rendered.min(), rendered.shape)
    slab_print(rendered / 255.)
