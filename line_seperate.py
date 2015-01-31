#/usr/bin/env python
#*-* coding: utf-8 *-*
from scipy import ndimage
import numpy as np
from PIL import Image as im


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

    def morph_all(self,):
        self.closed = ndimage.binary_closing(self.data)
        self.opened = ndimage.binary_opening(self.data)

    def calc_hist(self,):
        self.hist = np.sum(self.data, axis=1).astype('float')
        hist_mean = np.mean(self.hist)
        self.fft = abs(np.fft.rfft(self.hist - hist_mean))
        max_harm = np.argmax(self.fft)
        assert max_harm > 0

        self.best_harmonic = self.ht // (1 + max_harm)
        self.gaus_hist = ndimage.filters.gaussian_filter1d(self.hist,
                    self.best_harmonic/16, truncate=4.0,  mode='constant',
                    cval=0)
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

        for i, val in enumerate(hist):
            if inpeak == False:
                if val > peakthresh:
                    print 'transition to in-peak @ ', i, val
                    inpeak = True
                    maxval = val
                    maxloc = i
                    mintosearch = i + min_dist_in_peak
                    # accept no zeros between i and i+mintosearch

            else: # inpeak == TRUE; look for max
                if val > maxval:
                    maxval = val
                    maxloc = i
                    mintosearch = i + min_dist_in_peak
                elif i > mintosearch and val <= zerothresh:
                    # leave peak and save the last baseline found
                    inpeak = False
                    print 'Found baseline @ ', maxloc
                    self.base_lines.append(maxloc)

        self.num_lines = len(self.base_lines)


    def separate_lines(self,):
        self.top_lines = []
        self.line_sep = [0]

        for i, base in enumerate(self.base_lines):
            # Find top lines
            if i == 0:  frm = 0
            else:   frm = self.line_sep[i]
            print " Searching for top line in range : ", frm+1, base
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

import sys
im = Image(sys.argv[1])

for row in im.data:
    for p in row[:80]:
        print {0:' ', 1:'#'}[p],
    print

#im.filter_noise()
im.calc_hist()
for l, i, j, k in zip(range(im.ht), im.hist, im.gaus_hist, im.d_gaus_hist):
    print l, i, j, k
im.find_baselines()
im.separate_lines()

for k, v in im.__dict__.items():
    print k, ': ',
    try:
        print v.shape
    except:
        print v

print "BEST HARMONIC", im.best_harmonic

for i in range(im.num_lines):
    print im.line_sep[i]
    print im.top_lines[i], im.base_lines[i]
print im.line_sep[-1]