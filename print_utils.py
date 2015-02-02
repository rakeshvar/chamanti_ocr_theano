# -*- coding: utf-8 -*-

def pprint(slab):
    if slab.max() == 255:
        pprint_(slab/255.)
    else:
        pprint_(slab)

def pprint_(slab):
    """
    Prints a 'slab' of printed 'text' using ascii.
    :param slab: A matrix of floats from [0, 1]
    """
    for ir, r in enumerate(slab):
        print('{:2d}¦'.format(ir), end='')
        for val in r:
            if   val < 0.0:  print('-', end='')
            elif val < .15:  print(' ', end=''),
            elif val < .35:  print('░', end=''),
            elif val < .65:  print('▒', end=''),
            elif val < .85:  print('▓', end=''),
            elif val <= 1.:  print('█', end=''),
            else:            print('+', end='')
        print('¦')

def pprint_ascii(nparr):
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

def pprint_binary(nparr):
    print('-' * (len(nparr[0]) + 5))
    for ir, r in enumerate(nparr):
        print('{:3d}|'.format(ir), end='')
        for p in r:
            print([' ', '#'][1 * p], end='')
        print('|')
    print('-' * (len(nparr[0]) + 5))
