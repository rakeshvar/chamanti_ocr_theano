import os
import pickle
from random import randrange
from collections import defaultdict, Counter

print("Loading the uni and bigram counts")
this_dir, this_filename = os.path.split(__file__)
corpus = os.path.join(this_dir, "data", "telugu.bigram")
beg_line, end_line, unicount, bicount = pickle.load(open(corpus, "rb"))

def get_word(length):
    char, sample_text = ' ', ''

    for j in range(length):
        char = list(bicount[char].elements())[randrange(unicount[char])]
        if char == end_line:
            char = ' '
        sample_text += char

    return sample_text