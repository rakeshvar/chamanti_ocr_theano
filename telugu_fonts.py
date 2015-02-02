#! /usr/bin/env python
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

SIZE, GHO, REPHA, PPU, SPACING, ABBR, BOLD = range(7)
font_properties = {
'Akshar Unicode':           [48, 'K', 'BB', 0, 1, 'Akshar', 1],
'Dhurjati':                 [48, 'K', 'BB', 0, 1, 'Dhurjati', 1],
'Gautami':                  [48, 'K', 'BB', 0, 1, 'Gautami', 1],
'Gidugu':                   [48, 'K', 'BR', 1, 1, 'Gidugu', 1],
'GIST-TLOTAmma':            [28, 'K', 'LR', 1, 1, 'Amma', 1],
'GIST-TLOTAmruta':          [28, 'K', 'LR', 1, 1, 'Amruta', 0],
'GIST-TLOTAtreya':          [28, 'K', 'LR', 1, 1, 'Atreya', 1],
'GIST-TLOTChandana':        [28, 'K', 'LR', 1, 1, 'Chandana', 0],
'GIST-TLOTDeva':            [28, 'K', 'LR', 1, 1, 'Deva', 0],
'GIST-TLOTDraupadi':        [28, 'K', 'LR', 1, 1, 'Draupadi', 1],
'GIST-TLOTGolkonda':        [28, 'K', 'LR', 1, 1, 'Golkonda', 0],
'GIST-TLOTKrishna':         [28, 'K', 'LR', 1, 1, 'Krishna', 1],
'GIST-TLOTManu':            [28, 'K', 'LR', 1, 1, 'Manu', 1],
'GIST-TLOTMenaka':          [28, 'K', 'LR', 1, 1, 'Menaka', 1],
'GIST-TLOTPavani':          [28, 'K', 'LR', 1, 1, 'Pavani', 0],
'GIST-TLOTPriya':           [22, 'K', 'LR', 1, 1, 'Priya', 0],
'GIST-TLOTRajan':           [28, 'K', 'LR', 1, 1, 'Rajan', 0],
'GIST-TLOTRajani':          [28, 'K', 'LR', 1, 1, 'Rajani', 0],
'GIST-TLOTSanjana':         [28, 'K', 'LR', 1, 1, 'Sanjana', 0],
'GIST-TLOTSitara':          [28, 'K', 'LR', 1, 1, 'Sitara', 0],
'GIST-TLOTSwami':           [28, 'K', 'LR', 1, 1, 'Swami', 0],
'GIST-TLOTVennela':         [28, 'K', 'LR', 1, 1, 'Vennela', 1],
'Gurajada':                 [48, 'K', 'BR', 1, 1, 'Gurajada', 1],
'LakkiReddy':               [48, 'K', 'BB', 0, 1, 'LakkiReddy', 1],
'Lohit Telugu':             [48, 'K', 'BB', 0, 1, 'Lohit', 1],
'Mallanna':                 [48, 'T', 'BB', 0, 1, 'Mallanna', 1],
'Mandali':                  [48, 'T', 'LB', 0, 1, 'Mandali', 1],
'Nandini':                  [48, 'K', 'LL', 0, 1, 'Nandini', 1],
'NATS':                     [48, 'K', 'BR', 1, 1, 'NATS', 1],
'Noto Sans Telugu':         [48, 'K', 'BR', 0, 1, 'Noto', 1],
'NTR':                      [48, 'K', 'BB', 1, 1, 'NTR', 1],
'Peddana':                  [48, 'K', 'BR', 0, 1, 'Peddana', 1],
'Ponnala':                  [48, 'K', 'BB', 0, 1, 'Ponnala', 1],
'Pothana2000':              [48, 'K', 'BR', 1, 1, 'Pothana', 1],
'Ramabhadra1':              [48, 'T', 'BB', 0, 1, 'Ramabhadra', 1],
'RamaneeyaWin':             [48, 'K', 'BB', 0, 1, 'Ramaneeya', 1],
'Ramaraja':                 [48, 'K', 'BB', 0, 1, 'Ramaraja', 1],
'RaviPrakash':              [48, 'K', 'BB', 0, 1, 'RaviPrakash', 1],
'Sree Krushnadevaraya':     [48, 'T', 'BB', 0, 1, 'Krushnadeva', 1],
'Subhadra':                 [48, 'T', 'BB', 0, 1, 'Subhadra', 1],
'Suguna':                   [48, 'T', 'BB', 1, 2, 'Suguna', 1],
'Suranna':                  [48, 'T', 'LR', 0, 1, 'Suranna', 1],
'SuraVara_Samhita':         [48, 'K', 'BB', 0, 1, 'Samhita', 1],
'SURAVARA_Swarna':          [48, 'K', 'BB', 0, 1, 'Swarna', 1],
'Suravaram':                [48, 'K', 'BR', 1, 1, 'Suravaram', 1],
'TenaliRamakrishna':        [48, 'K', 'BB', 0, 1, 'Tenali', 1],
'Timmana':                  [48, 'K', 'BB', 0, 1, 'Timmana', 0],
'Vajram':                   [48, 'K', 'BB', 0, 1, 'Vajram', 1],
'Vani':                     [48, 'K', 'BR', 0, 1, 'Vani', 1],
'Vemana2000':               [48, 'K', 'BR', 1, 1, 'Vemana', 1]
}


if __name__ == '__main__':
    from gi.repository import PangoCairo

    font_map = PangoCairo.font_map_get_default()
    families = font_map.list_families()
    font_names = [f.get_name() for f in families]

    for f in sorted(font_names):
        if f in font_properties:
            print('\n{}{}'.format(f, font_properties[f]))
        else:
            print("[X]{}\t".format(f))

    for f in font_properties:
        if f in font_names:
            print("[✓]{}\t".format(f), end='')
        else:
            print("\n[!]{} Not Installed".format(f))
