#/usr/bin/env python3
#*-* coding: utf-8 *-*

from scipy import ndimage
import numpy as np
from PIL import Image as im

def log(*args, **kwargs):
    if False:
        print(*args, **kwargs)

class Image():
    def __init__(self, path):
        self.path = path
        self.img = im.open(path)
        self.wd, self.ht = self.img.size
        self.data = np.asarray(self.img.getdata()).reshape((self.ht, self.wd)) 
        self.data //= 255
        self.data = 1 - self.data

    def filter_noise(self,):
        self.data = ndimage.median_filter(self.data, 3)

    def calc_hist(self,):
        hist_ = np.sum(self.data, axis=1).astype('float')
        hist_mean = np.mean(hist_)
        self.fft = abs(np.fft.rfft(hist_ - hist_mean))
        max_harm = int(np.argmax(self.fft))
        self.best_harmonic = self.ht // (1 + max_harm)
        assert max_harm > 0

        self.closed = ndimage.binary_closing(self.data, structure=np.ones((1, self.best_harmonic//4)))
        self.hist = np.sum(self.closed, axis=1).astype(float)
        self.gaus_hist = ndimage.filters.gaussian_filter1d(self.hist,
                    self.best_harmonic/16, mode='constant',
                    cval=0,
                    truncate=4.0,
        )
        self.d_gaus_hist = ndimage.filters.convolve(self.gaus_hist, [-1, 0, 1])

    def find_baselines(self,):
        hist = self.d_gaus_hist
        gmaxval = np.max(hist)
        maxloc = np.argmax(hist)
        peakthresh = gmaxval / 10.0
        zerothresh = gmaxval / 50.0
        inpeak = False
        min_dist_in_peak = self.best_harmonic / 2.0
        self.base_lines = []
        log("Max Hist: {:.2f} Peakthresh: {:.2f} Zerothresh: {:.2f}"
              "Min Dist in Peak: {:.2f}".format(gmaxval, peakthresh, zerothresh, min_dist_in_peak))

        for i, val in enumerate(hist):
            if not inpeak:
                if val > peakthresh:
                    inpeak = True
                    maxval = val
                    maxloc = i
                    mintosearch = i + min_dist_in_peak
                    log('\ntransition to in-peak: mintosearch : ', mintosearch, end='')
                    # accept no zeros between i and i+mintosearch

            else:  #  in peak, look for max
                if val > maxval:
                    maxval = val
                    maxloc = i
                    mintosearch = i + min_dist_in_peak
                    log('\nMoved mintosearch to', mintosearch, end='')
                elif i > mintosearch and val <= zerothresh:
                    # leave peak and save the last baseline found
                    inpeak = False
                    log('\nFound baseline #', maxloc, end='')
                    self.base_lines.append(maxloc)

            log(' @{}'.format(i), end='')

        if inpeak:
            self.base_lines.append(maxloc)
            log('\nFound baseline #', maxloc, end='')

        self.num_lines = len(self.base_lines)

    def separate_lines(self,):
        self.top_lines = []
        self.line_sep = [0]

        for i, base in enumerate(self.base_lines):
            # Find top lines
            if i == 0:  frm = 0
            else:   frm = self.line_sep[i]
            log(" Searching for top line in range : ", frm+1, base)
            top_at = np.argmin(self.d_gaus_hist[frm+1:base])
            self.top_lines.append(frm + 1 + top_at)

            # Find line separation
            if i+1 < self.num_lines:
                to = self.base_lines[i+1]
            else:
                to = self.ht
            sep_at = np.argmin(self.gaus_hist[base+1:to])
            self.line_sep.append(base + 1 + sep_at)

    def get_line(self, i):
        return self.data[self.line_sep[i]:self.line_sep[i+1]]


################################ UNIT TEST ################################

if __name__ == '__main__':
    import sys
    from print_utils import pprint
    from PIL import ImageDraw as id

    img = Image(sys.argv[1])

    img.filter_noise()
    img.calc_hist()
    for l, i, j, k in zip(range(img.ht),
                          img.hist,
                          img.gaus_hist,
                          img.d_gaus_hist):
        log("{:4d} {:7.2f} {:7.2f} {:7.2f}".format(l, i, j, k))
    log()

    img.find_baselines()
    img.separate_lines()

    print('\nImage Properties:')
    for k in sorted(img.__dict__):
        v = getattr(img, k)
        try:
            print(k, ':', v.shape, '(shape)')
        except AttributeError:
            print(k, ':', v)
    print()

    ################################## Show Image with Lines
    img_col = img.img.convert("RGB")
    draw = id.Draw(img_col)
    def line(ats, col):
        for at in ats:
            draw.line((0, at, img.wd, at), fill=col, width=2)

    line(img.top_lines,  (255,0,0))
    line(img.base_lines, (0,255,0))
    line(img.line_sep, (0,0,255))
    img_col.show()