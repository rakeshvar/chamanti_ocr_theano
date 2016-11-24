import bisect
import os
import pickle
from itertools import accumulate
from random import random
import numpy as np

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

    random_location = int(accumulated_counts[-1] * random())
    random_location = bisect.bisect(accumulated_counts, random_location)
    return followers[random_location]


def get_next_char_fair(char):
    try:
        followers, accumulated_counts = bicount_listed[char]
    except KeyError:
        followers, counts = zip(*bicount[char].items())
        accumulated_counts = list(accumulate(counts))
        bicount_listed[char] = followers, accumulated_counts

    random_location1 = int(accumulated_counts[-1] * random())
    random_location = bisect.bisect(accumulated_counts, random_location1)
    # if len(accumulated_counts) == 5 and char == 'న్మో':
    #     print("{}) {:5d} < {:5d} picks {:5d} from {}".format(len(accumulated_counts),
    #         random_location1, accumulated_counts[-1], random_location,  accumulated_counts),
    #           end='->')
    current_count = accumulated_counts[random_location]
    if random_location>0:
        current_count -= accumulated_counts[random_location-1]
    half_current_count = current_count // 2
    for i in range(random_location, len(accumulated_counts)):
        accumulated_counts[i] -= half_current_count
    # if len(accumulated_counts) == 5 and char == 'న్మో':
    #     print(accumulated_counts, " removed {:4d}/2 = {:4d} {}".format(current_count,
    #                                                                    half_current_count,
    #                                                                    char))
    return followers[random_location]


def get_next_char_fair_numpy(char):
    try:
        followers, accumulated_counts = bicount_listed[char]
    except KeyError:
        followers, counts = zip(*bicount[char].items())
        accumulated_counts = np.cumsum(counts)
        bicount_listed[char] = followers, accumulated_counts

    random_location = int(accumulated_counts[-1] * random())
    random_location = bisect.bisect(accumulated_counts, random_location)
    current_count = accumulated_counts[random_location]
    if random_location>0:
        current_count -= accumulated_counts[random_location-1]
    accumulated_counts[random_location:] -= current_count//2
    return followers[random_location]


def get_next_char_numpy(char):
    if char in bicount_listed:
        followers, accumulated_counts = bicount_listed[char]
    else:
        followers, counts = zip(*bicount[char].items())
        accumulated_counts = np.cumsum(counts)
        bicount_listed[char] = followers, accumulated_counts

    random_location = int(accumulated_counts[-1] * random())
    # random_location = np.searchsorted(accumulated_counts, random_location, 'right')
    random_location = bisect.bisect(accumulated_counts, random_location)
    return followers[random_location]


def get_next_char_old(char):
    return list(bicount[char].elements())[int(random() * (unicount[char]))]


def get_word(length, fn=get_next_char):
    char, sample_text = ' ', ''

    for j in range(length):
        char = fn(char)
        if char == end_line:
            char = ' '
        sample_text += char

    return sample_text