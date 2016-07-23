import random
import indic_scribe as ind

import telugu as language

tenn = 5
ht = 45
buf = 5

def get_line(length=None):
    twist = random.uniform(-1, 1)/10
    font_prop = language.random_font()

    text = language.get_word(length)
    img = ind.scribe(text,
                     fontname=font_prop["font"],
                     size=48, #font_prop["size"],
                     style=font_prop["style"],
                     twist=twist,
                     ten=tenn)

    #img = ind.smartrim(img, ht, buf)

    return img, language.get_labels(text), twist, text, font_prop

if __name__ == '__main__':
    from print_utils import pprint

    try:
      while True:
        image, labels, angle, text, fp = get_line(3)
        pprint(image)
        print(image.shape)
        print(labels)
        print("Twist: {:.3f}".format(angle), fp)
        print(text)
        input()
    except (KeyboardInterrupt, EOFError):
        pass