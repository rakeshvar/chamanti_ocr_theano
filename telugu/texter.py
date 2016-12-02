import bisect
import os
import pickle
from itertools import accumulate
from random import random
import numpy as np

print("Loading the uni and bigram counts")
this_dir, this_filename = os.path.split(__file__)
corpus = os.path.join(this_dir, "data", "telugu.bigram")
beg_line, end_line, unigram_counts, bigram_counts = pickle.load(open(corpus, "rb"))

bi_acc_cache = {}
bi_acc_cache_np = {}

REDUCE_COUNT_BY_nTH = 8

def get_next_char(char):
    if char in bi_acc_cache:
        followers, accumulated_counts = bi_acc_cache[char]
    else:
        followers, counts = zip(*bigram_counts[char].items())
        accumulated_counts = tuple(accumulate(counts))
        bi_acc_cache[char] = followers, accumulated_counts

    loc = int(accumulated_counts[-1] * random())
    follower = bisect.bisect(accumulated_counts, loc)
    return followers[follower]


def get_next_char_decay(char):  # Nearly six times slower!
    try:
        followers, accumulated_counts = bi_acc_cache_np[char]
    except KeyError:
        followers, counts = zip(*bigram_counts[char].items())
        accumulated_counts = np.fromiter(accumulate(counts), dtype=np.int32)
        bi_acc_cache_np[char] = followers, accumulated_counts

    loc = np.int32(accumulated_counts[-1] * random())
    follower = bisect.bisect(accumulated_counts, loc)
    current_count = accumulated_counts[follower]
    if follower:
        current_count -= accumulated_counts[follower-1]

    if current_count > 1:
        if current_count < REDUCE_COUNT_BY_nTH:
            decrement = 1
        else:
            decrement = current_count//REDUCE_COUNT_BY_nTH

        accumulated_counts[follower:] -= decrement

    # if len(accumulated_counts) == 5 and char == 'ణ్ని':
    #     print("{}) {:5d} < {:5d} picks {:2d} removed {:4d}//{} = {:3d} from {} {}".format(
    #         len(accumulated_counts), loc, accumulated_counts[-1], follower,
    #         current_count, REDUCE_COUNT_BY_nTH, decrement, accumulated_counts, char))

    return followers[follower]


def get_word(length, getter=get_next_char, as_str=False):
    char, sample_text = ' ', []

    for j in range(length):
        char = getter(char)
        if char == end_line:
            char = ' '
        sample_text.append(char)

    if as_str:
        sample_text = ''.join(sample_text)

    return sample_text


def get_words(n, len, fn):
     for i in range(n):
         get_word(len, fn)