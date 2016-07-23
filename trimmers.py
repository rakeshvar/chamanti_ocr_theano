import numpy as np


def trim(nparr):
    good_rows = np.where(np.sum(nparr, axis=1) > 0)[0]
    good_cols = np.where(np.sum(nparr, axis=0) > 0)[0]

    try:
        return nparr[good_rows.min():good_rows.max() + 1,
                     good_cols.min():good_cols.max() + 1]
    except ValueError:
        return np.array([[]])


def horztrim(nparr, wd_buffer):
    ht, wd = nparr.shape

    good_cols = np.where(np.sum(nparr, axis=0) > 0)[0]

    if len(good_cols):
        lft, rgt = good_cols.min(), good_cols.max() + 1
    else:
        lft, rgt = wd_buffer, wd_buffer + 1

    lft = max(0, lft - wd_buffer)
    rgt = min(rgt + wd_buffer, wd)

    return nparr[:, lft:rgt]



def smartrim(nparr, target_ht, wd_buffer):
    ht, wd = nparr.shape
    assert ht >= target_ht

    good_rows = np.where(np.sum(nparr, axis=1) > 0)[0]
    good_cols = np.where(np.sum(nparr, axis=0) > 0)[0]

    if len(good_rows):
        top, bot = good_rows.min(), good_rows.max() + 1
        lft, rgt = good_cols.min(), good_cols.max() + 1
    else:
        top, bot, lft, rgt = 0, target_ht, wd_buffer, wd_buffer + 1

    ######## Center and Clip
    newtop = max(0, top + (bot - top - target_ht) // 2)
    newbot = newtop + target_ht
    if newbot > ht:
        print('Ht {}, top{}, bot{}, newtop{}, newbot{}'.format(ht, top, bot,
                                                               newtop, newbot))
        newbot = ht
        newtop = newbot - target_ht

    assert newbot - newtop == target_ht

    ######## Buffer
    lft = max(0, lft - wd_buffer)
    rgt = min(rgt + wd_buffer, wd)

    return nparr[newtop:newbot, lft:rgt]


