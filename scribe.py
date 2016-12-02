#! /usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Uses cffi_wrapper to render given text to image.
'''
import random

from scribe_interface import scribe_text
from trimmers import horztrim


def scribe_wrapper(text, fontname, styleid, size,
                   height, hbuffer, vbuffer,
                   twist):
    styles = '', ' Italic', ' Bold', ' Bold Italic'
    font_style = "{} {} {}".format(fontname, styles[styleid], size)

    if type(text) is list:
        text = ''.join(text)

    lines = text.split('\n')
    n_lines = len(lines)
    n_letters = max(len(line) for line in lines)
    line_ht = height / (n_lines+1)
    letter_wd = .7 * line_ht
    width = round((n_letters+2) * letter_wd)

    return scribe_text(text, font_style, width, height, hbuffer, vbuffer, twist)


class Scribe():
    def __init__(self, language, **kwargs):
        self.language = language
        self.height = kwargs["height"]
        self.vbuffer = kwargs["vbuffer"]
        self.hbuffer = kwargs["hbuffer"]
        self.maxangle = kwargs["maxangle"]
        self.nchars = kwargs["nchars_per_sample"]
        self.size = kwargs["size"]
        self.noise = kwargs["noise"]

    def get_text_image(self):
        twist = self.maxangle * random.uniform(-1, 1)
        fontname, rel_size, styleid = self.language.random_font()

        text = self.language.get_word(self.nchars)
        img = scribe_wrapper(text, fontname, styleid, self.size,
                             self.height, self.hbuffer, self.vbuffer, twist)

        img = horztrim(img, self.hbuffer)

        return img, self.language.get_labels(text)

    def __str__(self):
        return "Height:{} Buffers:v{} h{} Size:{}" \
               "\nAngle:{:.2f} Noise:{:.2f}" \
               "\nNumChars:{}".format(
            self.height, self.vbuffer, self.hbuffer, self.size,
            self.maxangle, self.noise, self.nchars
        )