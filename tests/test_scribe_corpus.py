#!/usr/bin/python3
'''
Given a corpus of unicode text. It will write each line to an image and
save the numpy arrays.
'''
import sys
import pickle

from scribe import scribe_wrapper
from utils import slab_print

import telugu as language

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

    for fontname in sorted(language.font_properties):
        [sz, gho, rep, ppu, spc, abbr, hasbold] = language.font_properties[fontname]

        for style in range(4 if hasbold else 2):
            x = scribe_wrapper(line, fontname, style, 32, 200, 5, 5, 0)
            y = language.get_labels(line)
            xs.append(x)
            ys.append(y)

            if printall or fontname is "Mallanna":
                print(fontname, style, ys[-1])
                print(xs[-1].shape)
                slab_print(xs[-1])

if in_file_name.startswith('/dev'):
    out_file_name = "tmp.pkl"
else:
    out_file_name = in_file_name.replace(".txt", ".pkl")

with open(out_file_name, 'wb') as f:
    pickle.dump({'x': xs, 'y': ys, 'nChars': len(language.symbols)}, f, -1)

print('nChars:', len(language.symbols))
print(out_file_name)