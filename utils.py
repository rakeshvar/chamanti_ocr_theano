# -*- coding: utf-8 -*-
import ast
import numpy as np
import sys


def slab_print_ascii(nparr):
    print('-' * (len(nparr[0]) + 5))
    for ir, r in enumerate(nparr):
        print('{:3d}|'.format(ir), end='')
        for c in r:
            if   c == 0:  v = ' '
            elif c < .2:  v = '.'
            elif c < .4:  v = '*'
            elif c < .6:  v = 'o'
            elif c < .8:  v = '0'
            elif c <  1:  v = '@'
            else:         v = '#'
            print(v, end='')
        print('|')
    print('-' * (len(nparr[0]) + 5))


def slab_print_binary(nparr):
    print('-' * (len(nparr[0]) + 5))
    for ir, r in enumerate(nparr):
        print('{:3d}|'.format(ir), end='')
        for p in r:
            print([' ', '#'][1 * p], end='')
        print('|')
    print('-' * (len(nparr[0]) + 5))


def slab_print(slab, col_names=None):
    """
    Prints a 'slab' of printed 'text' using ascii.
    :param slab: A matrix of floats from [0, 1]
    """
    if slab.max() == 255:
        slab1 = slab/255.
    else:
        slab1 = slab

    for ir, r in enumerate(slab1):
        print('{:2d}¦'.format(ir), end='')
        for val in r:
            if   val < 0.0:     print('-', end='')
            elif val < .15:     print(' ', end=''),
            elif val < .35:     print('░', end=''),
            elif val < .65:     print('▒', end=''),
            elif val < .85:     print('▓', end=''),
            elif val <= 1.:     print('█', end=''),
            else:               print('+', end='')
        print('¦ {}'.format(col_names[ir] if col_names else ''))


class Printer():
    def __init__(self, symbols):
        """
        Creates a function that can print a predicted output of the CTC RNN
        It removes the blank characters (need to be set to n_classes),
        It also removes duplicates
        :param list symbols: list of symbols in the language encoding
        """
        self.symbols = symbols + ['_']
        self.n_classes = len(self.symbols) - 1

    def labels_to_chars(self, labels_out):
        return [self.symbols[l] for l in labels_out]

    def remove_blanks_repeats(self, labels):
        labels_out = []
        for il, l in enumerate(labels):
            if (l != self.n_classes) and (il == 0 or l != labels[il - 1]):
                labels_out.append(l)
        return labels_out

    def ylen(self, labels):
        return len(self.remove_blanks_repeats(labels))

    def show_labels(self, seq):
        labels = self.remove_blanks_repeats(seq)
        chars = self.labels_to_chars(labels)
        print(labels, ''.join(chars))
        return labels, chars

    def decode(self, softmax_firings):
        max_labels = np.argmax(softmax_firings, 0)
        seen_labels = self.remove_blanks_repeats(max_labels)
        return seen_labels

    def show_all(self, shown_seq, shown_img,
                 softmax_firings=None,
                 *aux_imgs):
        """
        Utility function to show the input and output and debug
        :param shown_seq: Labelings of the input
        :param shown_img: Input Image
        :param softmax_firings: Seen Probabilities (Excitations of Softmax)
        :param aux_imgs: List of pairs of images and names
        :return:
        """
        print('Shown : ', end='')
        labels, chars = self.show_labels(shown_seq)

        if softmax_firings is not None:
            print('Seen  : ', end='')
            seen_labels = self.decode(softmax_firings)
            self.show_labels(seen_labels)

        print('Image Shown:')
        slab_print(shown_img)

        if softmax_firings is not None:
            seen_labels = list(set(seen_labels) - set(labels))
            seen_chars = self.labels_to_chars(seen_labels)
            l = labels + [self.n_classes] + seen_labels
            c = chars + ['blank'] + seen_chars
            print('SoftMax Firings:')
            slab_print(softmax_firings[l], c)

        for aux_img, aux_name, *col_names in aux_imgs:
            col_names = self.labels_to_chars(col_names[0]) if col_names else None
            print(aux_name)
            slab_print(aux_img, col_names)


def insert_blanks(y, blank, num_blanks_at_start=1):
    # Insert blanks at alternate locations in the labelling (blank is blank)
    y1 = [blank] * num_blanks_at_start
    for char in y:
        y1 += [char, blank]
    return y1


def read_args(files, default='configs/default.ast'):
    with open(default, 'r') as dfp:
        args = ast.literal_eval(dfp.read())

    for config_file in files:
        with open(config_file, 'r') as cfp:
            override_args = ast.literal_eval(cfp.read())

        for key in args:
            if key in override_args:
                try:
                    args[key].update(override_args[key])
                except AttributeError:
                    args[key] = override_args[key]

    return args


def pprint_probs(probs):
    for row in (10 * probs).astype(int):
        for val in row:
            print('{:+04d}'.format(val), end='')
        print()


def write_dict(d, f=sys.stdout, level=0):
    tabs = '\t' * level
    print(file=f)
    for k in sorted(d.keys()):
        v = d[k]
        print('{}{}: '.format(tabs, k), file=f, end='')
        if type(v) is dict:
            write_dict(v, f, level+1)
        else:
            print('{}'.format(v), file=f)