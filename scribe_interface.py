'''
A wrapper around functions to render text to images. 
Uses cairo via cffi.
Based on:
    https://pythonhosted.org/cairocffi/cffi_api.html#example-using-pango-through-cffi-with-cairocffi
    https://github.com/Kozea/cairocffi/issues/87
'''
import cffi
import array
import cairocffi
import numpy as np

ffi = cffi.FFI()
# ffi.include(cairocffi.ffi)
ffi.cdef('''
    typedef void cairo_t;
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

    PangoFontDescription* pango_font_description_new(void);

    void pango_font_description_set_family(
        PangoFontDescription *desc, const char *family);

    void pango_layout_set_font_description(
        PangoLayout *layout, const PangoFontDescription *desc);

    PangoFontDescription* pango_font_description_from_string (
        const char *str);

    void pango_font_description_set_size (
        PangoFontDescription *desc, int size);
''')
gobject = ffi.dlopen('gobject-2.0')
pango = ffi.dlopen('pango-1.0')
pangocairo = ffi.dlopen('pangocairo-1.0')

gobject_ref = lambda pointer: ffi.gc(pointer, gobject.g_object_unref)
units_from_double = pango.pango_units_from_double


def scribe_text(text, font_style,
                width, height,
                x_offset, y_offset,
                rotation):

    fmt = cairocffi.FORMAT_A8
    width = cairocffi.ImageSurface.format_stride_for_width(fmt, width)
    data = array.array('b', [0] * (height * width))
    surface = cairocffi.ImageSurface(fmt, width, height, data, width)
    # pangocairo.pango_cairo_set_antialias(cairocffi.ANTIALIAS_SUBPIXEL)

    context = cairocffi.Context(surface)
    context.translate(x_offset, y_offset)
    context.rotate(rotation)
    layout = gobject_ref(pangocairo.pango_cairo_create_layout(context._pointer))
    pango.pango_layout_set_text(layout, text.encode('utf8'), -1)

    font_desc = pango.pango_font_description_from_string(font_style.encode('utf8'))
    pango.pango_layout_set_font_description(layout, font_desc)
    # pango.pango_layout_set_spacing(spc * 32)

    pangocairo.pango_cairo_update_layout(context._pointer, layout)
    pangocairo.pango_cairo_show_layout(context._pointer, layout)
    # print(surface.get_width(), surface.get_height())

    return np.frombuffer(data, dtype=np.uint8).reshape((height, width))