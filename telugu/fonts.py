"""
File contains the properties of available Telugu Fonts as a dictionary.
Fields:
    Font Name
    Style of gho (Kannada/Telugu)
    Style of repha (Bottom/Left/Right)
    Has Special form for ppu
    Required Letter Spacing (Single/Double)
    Abbreviation
    Has Bold
"""

SIZE, GHO, REPHA, PPU, SPACING, BOLD, ABBR, = range(7)
font_properties = {
'Akshar Unicode':           [48, 'K', 'BB', 0, 1, 1, 'Akshar',  ],
'Dhurjati':                 [48, 'K', 'BB', 0, 1, 1, 'Dhurjati',],
'Gautami':                  [48, 'K', 'BB', 0, 1, 1, 'Gautami', ],
'Gidugu':                   [48, 'K', 'BR', 1, 1, 1, 'Gidugu',  ],
'GIST-TLOTAmma':            [28, 'K', 'LR', 1, 1, 1, 'Amma',    ],
'GIST-TLOTAmruta':          [28, 'K', 'LR', 1, 1, 0, 'Amruta',  ],
'GIST-TLOTAtreya':          [28, 'K', 'LR', 1, 1, 1, 'Atreya',  ],
'GIST-TLOTChandana':        [28, 'K', 'LR', 1, 1, 0, 'Chandana',],
'GIST-TLOTDeva':            [28, 'K', 'LR', 1, 1, 0, 'Deva',    ],
'GIST-TLOTDraupadi':        [28, 'K', 'LR', 1, 1, 1, 'Draupadi',],
'GIST-TLOTGolkonda':        [28, 'K', 'LR', 1, 1, 0, 'Golkonda',],
'GIST-TLOTKrishna':         [28, 'K', 'LR', 1, 1, 1, 'Krishna', ],
'GIST-TLOTManu':            [28, 'K', 'LR', 1, 1, 1, 'Manu',    ],
'GIST-TLOTMenaka':          [28, 'K', 'LR', 1, 1, 1, 'Menaka',  ],
'GIST-TLOTPavani':          [28, 'K', 'LR', 1, 1, 0, 'Pavani',  ],
'GIST-TLOTPriya':           [22, 'K', 'LR', 1, 1, 0, 'Priya',   ],
'GIST-TLOTRajan':           [28, 'K', 'LR', 1, 1, 0, 'Rajan',   ],
'GIST-TLOTRajani':          [28, 'K', 'LR', 1, 1, 0, 'Rajani',  ],
'GIST-TLOTSanjana':         [28, 'K', 'LR', 1, 1, 0, 'Sanjana', ],
'GIST-TLOTSitara':          [28, 'K', 'LR', 1, 1, 0, 'Sitara',  ],
'GIST-TLOTSwami':           [28, 'K', 'LR', 1, 1, 0, 'Swami',   ],
'GIST-TLOTVennela':         [28, 'K', 'LR', 1, 1, 1, 'Vennela', ],
'Gurajada':                 [48, 'K', 'BR', 1, 1, 1, 'Gurajada',],
'LakkiReddy':               [48, 'K', 'BB', 0, 1, 1, 'LakkiReddy',],
'Lohit Telugu':             [48, 'K', 'BB', 0, 1, 1, 'Lohit',   ],
'Mallanna':                 [48, 'T', 'BB', 0, 1, 1, 'Mallanna',],
'Mandali':                  [48, 'T', 'LB', 0, 1, 1, 'Mandali', ],
'Nandini':                  [48, 'K', 'LL', 0, 1, 1, 'Nandini', ],
'NATS':                     [48, 'K', 'BR', 1, 1, 1, 'NATS',    ],
'Noto Sans Telugu':         [48, 'K', 'BR', 0, 1, 1, 'Noto',    ],
'NTR':                      [48, 'K', 'BB', 1, 1, 1, 'NTR',     ],
'Peddana':                  [48, 'K', 'BR', 0, 1, 1, 'Peddana', ],
'Ponnala':                  [48, 'K', 'BB', 0, 1, 1, 'Ponnala', ],
'Pothana2000':              [48, 'K', 'BR', 1, 1, 1, 'Pothana', ],
'Ramabhadra1':              [48, 'T', 'BB', 0, 1, 1, 'Ramabhadra',  ],
'RamaneeyaWin':             [48, 'K', 'BB', 0, 1, 1, 'Ramaneeya',   ],
'Ramaraja':                 [48, 'K', 'BB', 0, 1, 1, 'Ramaraja',    ],
'RaviPrakash':              [48, 'K', 'BB', 0, 1, 1, 'RaviPrakash', ],
'Sree Krushnadevaraya':     [48, 'T', 'BB', 0, 1, 1, 'Krushnadeva', ],
'Subhadra':                 [48, 'T', 'BB', 0, 1, 1, 'Subhadra',    ],
'Suguna':                   [48, 'T', 'BB', 1, 2, 1, 'Suguna',  ],
'Suranna':                  [48, 'T', 'LR', 0, 1, 1, 'Suranna', ],
'SuraVara_Samhita':         [48, 'K', 'BB', 0, 1, 1, 'Samhita', ],
'SURAVARA_Swarna':          [48, 'K', 'BB', 0, 1, 1, 'Swarna',  ],
'Suravaram':                [48, 'K', 'BR', 1, 1, 1, 'Suravaram',],
'TenaliRamakrishna':        [48, 'K', 'BB', 0, 1, 1, 'Tenali',  ],
'Timmana':                  [48, 'K', 'BB', 0, 1, 0, 'Timmana', ],
'Vajram':                   [48, 'K', 'BB', 0, 1, 1, 'Vajram',  ],
'Vani':                     [48, 'K', 'BR', 0, 1, 1, 'Vani',    ],
'Vemana2000':               [48, 'K', 'BR', 1, 1, 1, 'Vemana',  ],
}

font_properties_list = list(font_properties.items())

import random


def random_font():
    font, properties = random.choice(font_properties_list)
    style = random.randrange(4 if properties[BOLD] else 2)

    return font, properties[SIZE], style


if __name__ == '__main__':
    from gi.repository import PangoCairo

    font_map = PangoCairo.font_map_get_default()
    families = font_map.list_families()
    font_names = [f.get_name() for f in families]

    for f in sorted(font_names):
        if f in font_properties:
            print('\n{}{}'.format(f, font_properties[f]))
        else:
            print("[X]{}".format(f), end='\t')

    print()
    for f in sorted(font_properties.keys()):
        if f in font_names:
            print("[✓]{}".format(font_properties[f][ABBR]), end=' ')
        else:
            print("\n[!]{} NOT INSTALLED".format(f))
