import sys
import scribe
from trimmers import trim
from utils import slab_print
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
    x = scribe.scribe(txt, font, tenn)
    print(language.font_properties[font][fonts.ABBR])
    slab_print(trim(x))
    # pprint(indic_scribe.smartrim(x, tenn*3, tenn//2))