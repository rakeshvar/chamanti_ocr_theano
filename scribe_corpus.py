#!/usr/bin/python3

import sys
import pickle

import indic_scribe as scribe
from labeler_basic import tel2int, num_labels
from print_utils import pprint
from telugu_fonts import font_properties

if len(sys.argv) < 2:
    print("Usage:\n" + sys.argv[0] + " text_file [printall=0]")
    sys.exit()

in_file_name = sys.argv[1]
with open(in_file_name) as fin:
    print("Opening ", sys.argv[1])
    text = fin.read()

printall = True if len(sys.argv) > 2 else False

xs, ys = [], []

for line in text.split('\n'):
    print('\n', line)

    for fontname in sorted(font_properties):
        [sz, gho, rep, ppu, spc, abbr, hasbold] = font_properties[fontname]

        for style in range(4 if hasbold else 2):
            x = scribe.scribe(line, fontname, 5, style, sz, spc)
            x = scribe.smartrim(x, 36, 5)
            y = tel2int(line)
            xs.append(x)
            ys.append(y)

            if printall or fontname is "Mallanna":
                print(fontname, style, ys[-1])
                print(xs[-1].shape)
                pprint(xs[-1])


out_file_name = in_file_name.replace(".txt", ".pkl")
with open(out_file_name, 'wb') as f:
    pickle.dump({'x': xs, 'y': ys, 'nChars': num_labels}, f, -1)

print('nChars:', num_labels)