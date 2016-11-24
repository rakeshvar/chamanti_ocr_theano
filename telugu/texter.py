import bisect
import os
import pickle
from itertools import accumulate
from random import randrange

print("Loading the uni and bigram counts")
this_dir, this_filename = os.path.split(__file__)
corpus = os.path.join(this_dir, "data", "telugu.bigram")
beg_line, end_line, unicount, bicount = pickle.load(open(corpus, "rb"))

bicount_listed = {}


def get_next_char(char):
    if char in bicount_listed:
        followers, accumulated_counts = bicount_listed[char]
    else:
        followers, counts = zip(*bicount[char].items())
        accumulated_counts = tuple(accumulate(counts))
        bicount_listed[char] = followers, accumulated_counts

    random_location = randrange(unicount[char])
    random_location = bisect.bisect(accumulated_counts, random_location)
    return followers[random_location]

def get_next_char_old(char):
    return list(bicount[char].elements())[randrange(unicount[char])]


def get_word(length, fn=get_next_char):
    char, sample_text = ' ', ''

    for j in range(length):
        char = fn(char)
        if char == end_line:
            char = ' '
        sample_text += char

    return sample_text

def get_words(n, len, fn):
    fn = {"old": get_next_char_old, "new": get_next_char}[fn]
    return [get_word(len, fn) for i in range(n)]