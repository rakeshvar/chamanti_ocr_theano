import sys
import indic_scribe
from print_utils import pprint
import telugu as language
import telugu.fonts as fonts

if len(sys.argv) < 2:
    print("Usage:\n"
          "{0} text_file"
          "\n or \n"
          "{0} <(echo 'text')".format(sys.argv[0]))
    sys.exit()

corpus_file = sys.argv[1]
with open(corpus_file) as fin:
    print("Opening ", corpus_file)
    txt = fin.read()

try:
    tenn = int(sys.argv[2])
except IndexError:
    tenn = 10

for font in sorted(language.font_properties):
    x = indic_scribe.scribe(txt, font, tenn)
    print(language.font_properties[font][fonts.ABBR])
    pprint(indic_scribe.trim(x))
    # pprint(indic_scribe.smartrim(x, tenn*3, tenn//2))