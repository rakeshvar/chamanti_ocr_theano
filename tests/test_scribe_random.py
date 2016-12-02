import sys
sys.path.append("..")

from utils import slab_print, read_args
import telugu as language
import scribe

args = read_args(sys.argv[1:],  default='../configs/default.ast')
scriber = scribe.Scribe(language, **args['scribe_args'])

try:
  while True:
    image, labels = scriber.get_text_image()
    slab_print(image)
    print(image.shape)
    print(labels)
    # print("Twist: {:.3f}".format(angle), fp)
    # print(text)
    print(scriber)
    print("Press Enter to continue and Ctrl-D to quit.")
    input()
except (KeyboardInterrupt, EOFError):
    pass