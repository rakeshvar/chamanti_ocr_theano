import random
import indic_scribe as ind

import telugu as language

tenn = 10
ht = 45
buf = 5

def get_line(length=None):
    twist = random.random()
    font_prop = language.random_font()

    text = language.get_word(length)
    img = ind.scribe(text,
                     fontname=font_prop["font"],
                     size=font_prop["size"],
                     style=font_prop["style"],
                     twist=twist,
                     ten=tenn)

    #img = ind.smartrim(img, ht, buf)

    return img, language.get_labels(text), twist, text, font_prop

if __name__ == '__main__':
    from print_utils import pprint
    image, labels, angle, text, fp = get_line(3)
    pprint(image)
    print(labels)
    print(angle, fp)
    print(text)