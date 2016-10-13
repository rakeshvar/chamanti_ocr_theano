'''
A wrapper around functions to render text to images. 
Uses cairo via cffi.
Based on:
    https://pythonhosted.org/cairocffi/cffi_api.html#example-using-pango-through-cffi-with-cairocffi
    https://github.com/Kozea/cairocffi/issues/87
'''
import cffi
# import cairocffi

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
