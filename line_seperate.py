#/usr/bin/env python3
#*-* coding: utf-8 *-*

import numpy as np
from scipy import ndimage as nd
from PIL import Image as im
from scipy.ndimage import interpolation as inter

if False:
    log = print
else:
    log = lambda *_, **__: None

class Page():
    def __init__(self, path):
        self.path = path
        self.orig = im.open(path)
        wd, ht = self.orig.size
        self.data = np.asarray(self.orig.getdata()).reshape((ht, wd))
        self.data //= 255
        self.data = 1 - self.data

    def filter_noise(self,):
        self.data = nd.median_filter(self.data, 3)

    def skew_correct(self,):
        angles = np.linspace(-2, 2, 21)
        best_score = -1
        for i, a in enumerate(angles):
            data = inter.rotate(self.data, a, reshape=0, order=0)
            hist = np.sum(data, axis=1)
            score = np.sum((hist[1:]-hist[:-1])**2)
            print(i, a, score, best_score)
            if score > best_score:
                self.angle = a
                self.data = data
                best_score = score
        print("Angle: ", self.angle)
        self.ht, self.wd = self.data.shape
        self.img = im.fromarray(255*(1-self.data).astype("uint8")).convert("RGB")

    def calc_hist(self,):
        hist_ = np.sum(self.data, axis=1).astype('float')
        hist_mean = np.mean(hist_)
        self.fft = abs(np.fft.rfft(hist_ - hist_mean))
        max_harm = int(np.argmax(self.fft))
        self.best_harmonic = self.ht // (1 + max_harm)
        assert max_harm > 0

        self.closed = nd.binary_closing(self.data,
        	structure=np.ones((1, self.best_harmonic//4)))
        self.hist = np.sum(self.closed, axis=1).astype(float)
        self.gaus_hist = nd.filters.gaussian_filter1d(self.hist,
                    self.best_harmonic/16, mode='constant',
                    cval=0,
                    truncate=4.0,
        )
        self.d_gaus_hist = nd.filters.convolve(self.gaus_hist, [-1, 0, 1])

    def get_gaus_hist_image(self, width=100):
        hist = 100 * self.gaus_hist / np.max(self.gaus_hist)
        appendage = np.zeros((self.ht, width), dtype='uint8')
        for i, h in enumerate(hist.astype('int')):
            appendage[i,:h] = 255
        return 255-appendage
    	
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
                    # log('\nMoved mintosearch to', mintosearch, end='')
                elif i > mintosearch and val <= zerothresh:
                    # leave peak and save the last baseline found
                    inpeak = False
                    log('\nFound baseline #', maxloc, end='')
                    self.base_lines.append(maxloc)

            # log(' @{}'.format(i), end='')

        if inpeak:
            self.base_lines.append(maxloc)
            log('\nFound baseline #', maxloc, end='')

        self.num_lines = len(self.base_lines)

    def separate_lines(self,):
        self.top_lines = []
        self.line_sep = [np.where(self.gaus_hist[0:self.base_lines[0]]==0)[0][-1]]
        log(self.base_lines)

        for i, base in enumerate(self.base_lines):
            # Find top lines
            if i == 0:  frm = 0
            else:   frm = self.line_sep[i]
            log(" Searching for top line in range : ", frm, base)
            top_at = np.argmin(self.d_gaus_hist[frm:base])
            self.top_lines.append(frm + top_at)
            log(" Top at: ", top_at, frm + top_at)

            # Find line separation
            if i+1 < self.num_lines:
                to = self.base_lines[i+1]
            else:
                to = self.ht
            sep_at = np.argmin(self.gaus_hist[base+1:to])
            self.line_sep.append(base + 1 + sep_at)
            log(" Line Sep at ", sep_at, base + 1 + sep_at)

    def get_line(self, i):
        return self.data[self.line_sep[i]:self.line_sep[i+1]]



################################ UNIT TEST ################################

if __name__ == '__main__':
    import sys
    from PIL import ImageDraw as id

    page = Page(sys.argv[1])
    page.filter_noise()
    page.skew_correct()
    page.calc_hist()
    for l, i, j, k in zip(range(page.ht),
                          page.hist,
                          page.gaus_hist,
                          page.d_gaus_hist):
        log("{:4d} {:7.2f} {:7.2f} {:7.2f}".format(l, i, j, k))
    log()

    page.find_baselines()
    page.separate_lines()

    print('\nImage Properties:')
    for k in sorted(page.__dict__):
        v = getattr(page, k)
        try:
            print(k, ':', v.shape, '(shape)')
        except AttributeError:
            print(k, ':', v)
    print()

    ################################## Show Image with Lines
    img_stk = im.new('RGB', (page.wd+100, page.ht))
    img_stk.paste(page.img, (0, 0))
    img_app = im.fromarray(page.get_gaus_hist_image(100))
    img_stk.paste(img_app, (page.wd, 0))
    draw = id.Draw(img_stk)

    def line(ats, col):
        for at in ats:
            draw.line((0, at, page.wd+100, at), fill=col, width=2)

    line(page.top_lines,  (255,0,0))
    line(page.base_lines, (0,255,0))
    line(page.line_sep,   (0,0,255))
    img_stk.show()