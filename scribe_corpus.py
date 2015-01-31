#!/usr/bin/python

import indic_scribe as scribe
import sys
import pickle
from telugu_fonts import font_properties

if len(sys.argv) < 2:
    print("Usage:\n" + sys.argv[0] + " text_file")
    sys.exit()

in_file_name = sys.argv[1]
with open(in_file_name) as fin:
    print("Opening ", sys.argv[1])
    text = fin.read().decode('utf8')

xs = []
ys = []

for line in text.split('\n'):
    print (line)
    for fontname in sorted(font_properties):
        x = scribe.scribe_trim(line, fontname, 5)
        y = scribe.tel2int(line)
        scribe.pprint(x)
        print(y)
        xs.append(x)
        ys.append(y)
        # break


out_file_name = in_file_name.replace(".txt", ".pkl")
with open(out_file_name, 'wb') as f:
    pickle.dump({'x': xs, 'y': ys, 'nChars': len(scribe.all_chars)}, f, -1)

print('nChars:', len(scribe.all_chars))