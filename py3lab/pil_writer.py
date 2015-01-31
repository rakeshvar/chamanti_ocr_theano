#!/usr/bin/env python3
#-*- coding:utf8 -*-

from PIL import Image, ImageFont, ImageDraw

im = Image.new("RGB",(160, 160))

draw = ImageDraw.Draw(im)

font_telugu = ImageFont.truetype("/usr/share/fonts/truetype/ttf-indic-fonts-core/Pothana2000.ttf",50)
text_telugu = "నిత్య"

font_hindi = ImageFont.truetype("/usr/share/fonts/truetype/ttf-indic-fonts-core/gargi.ttf",50)
text_hindi = "नित्य"

draw.text((10, 10), text_telugu, font=font_telugu)
draw.text((10, 90), text_hindi, font=font_hindi)
im.show()

