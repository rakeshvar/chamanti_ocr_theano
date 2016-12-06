from .fonts import font_properties, font_properties_list, random_font
from .texter import get_word
from .labeler_cv import get_labels, symbols


def select_labeler(name):
    global get_labels, symbols

    if name in (0, "unicode", "uni"):
        from .labeler_unicode import get_labels, symbols
    elif name in (1, "cv", "iast"):
        from .labeler_cv import get_labels, symbols
    elif name in (2, "glyph", "glyp", "glp"):
        from .labeler_glyph import get_labels, symbols
    else:
        raise ValueError("Could not recognize ", name)