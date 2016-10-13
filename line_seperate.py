# /usr/bin/env python3
#*-* coding: utf-8 *-*
'''
Detects lines in a binary text image.
'''
import numpy as np
from scipy import ndimage as nd
from PIL import Image as im
from PIL import ImageDraw as id
from scipy.ndimage import interpolation as inter

if False:
    log = print
else:
    log = lambda *_, **__: None


class Page():
    def __init__(self, path):
        self.path = path
        self.orig = im.open(path)
        self.wd, self.ht = self.orig.size
        self.imgarr = np.asarray(self.orig.getdata()).reshape((self.ht, self.wd))
        self.imgarr //= 255
        self.imgarr = 1 - self.imgarr

        self.angle = None
        self.fft, self.best_harmonic, self.closed = [None] * 3
        self.hist, self.gauss_hist, self.d_gauss_hist = [None] * 3
        self.base_lines, self.top_lines, self.line_sep = [None] * 3
        self.num_lines = None

    def process(self):
        self.filter_noise()
        self.skew_correct()
        self.calc_hist()
        self.find_baselines()
        self.separate_lines()

    def filter_noise(self, ):
        self.imgarr = nd.median_filter(self.imgarr, size=3)

    def skew_correct(self, ):
        best_score = -1
        for a in np.linspace(-2, 2, 21):
            data = inter.rotate(self.imgarr, a, reshape=0, order=0)
            hist = np.sum(data, axis=1)
            score = np.sum((hist[1:] - hist[:-1]) ** 2)
            if score > best_score:
                self.angle = float(a)
                self.imgarr = data
                best_score = score

        print("Angle: ", self.angle)
        self.ht, self.wd = self.imgarr.shape
        self.img = im.fromarray(255 * (1 - self.imgarr).astype("uint8")).convert("RGB")

    def calc_hist(self, ):
        hist_ = np.sum(self.imgarr, axis=1).astype('float')
        hist_mean = np.mean(hist_)
        self.fft = abs(np.fft.rfft(hist_ - hist_mean))
        max_harm = int(np.argmax(self.fft))
        self.best_harmonic = self.ht // (1 + max_harm)
        assert max_harm > 0

        self.closed = nd.binary_closing(self.imgarr, structure=np.ones((1, self.best_harmonic // 4)))
        self.hist = np.sum(self.closed, axis=1).astype("float")
        self.gauss_hist = nd.filters.gaussian_filter1d(
            self.hist,
            self.best_harmonic / 16, mode='constant',
            cval=0,
            truncate=2.0)
        self.d_gauss_hist = nd.filters.convolve(self.gauss_hist, [-1, 0, 1])

    def find_baselines(self, ):
        d_hist = self.d_gauss_hist
        gmaxval = np.max(d_hist)
        maxloc = np.argmax(d_hist)
        peakthresh = gmaxval / 10.0
        zerothresh = gmaxval / 50.0
        inpeak = False
        min_dist_in_peak = self.best_harmonic / 2.0
        self.base_lines = []
        log("Max Hist: {:.2f} Peakthresh: {:.2f} Zerothresh: {:.2f} Min Dist in Peak: {:.2f}"
            "".format(gmaxval, peakthresh, zerothresh, min_dist_in_peak))

        for irow, val in enumerate(d_hist):
            if not inpeak:
                if val > peakthresh:
                    inpeak = True
                    maxval = val
                    maxloc = irow
                    mintosearch = irow + min_dist_in_peak
                    log('\ntransition to in-peak: mintosearch : ', mintosearch, end='')
                    # accept no zeros between i and i+mintosearch

            else:  # in peak, look for max
                if val > maxval:
                    maxval = val
                    maxloc = irow
                    mintosearch = irow + min_dist_in_peak
                    log('\nMoved mintosearch to', mintosearch, end='')
                elif irow > mintosearch and val <= zerothresh:
                    # leave peak and save the last baseline found
                    inpeak = False
                    log('\nFound baseline #', maxloc, end='')
                    self.base_lines.append(maxloc)

            log(' @{}'.format(irow), end='')

        if inpeak:
            self.base_lines.append(maxloc)
            log('\nFound baseline #', maxloc, end='')

        self.num_lines = len(self.base_lines)

    def separate_lines(self, ):
        self.top_lines = []
        self.line_sep = [np.where(self.gauss_hist[0:self.base_lines[0]] == 0)[0][-1]]
        log(self.base_lines)

        for ibase, base in enumerate(self.base_lines):
            # Find top lines
            frm = 0 if ibase == 0 else self.line_sep[ibase]
            log(" Searching for top line in range : ", frm, base)
            top_at = np.argmin(self.d_gauss_hist[frm:base])
            self.top_lines.append(frm + top_at)
            log(" Top at: ", top_at, frm + top_at)

            # Find line separation
            to = self.base_lines[ibase + 1] if ibase + 1 < self.num_lines else self.ht
            sep_at = np.argmin(self.gauss_hist[base + 1:to])
            self.line_sep.append(base + 1 + sep_at)
            log(" Line Sep at ", sep_at, base + 1 + sep_at)

    def get_line(self, iline):
        return self.imgarr[self.line_sep[iline]:self.line_sep[iline + 1]]

    def get_info(self):
        ret = (
            "\nImage: {} "
            "\nHeight, Width: {}, {}"
            "\nShapes: Image Array:{} closed:{}"
            "\nRotated by angle: {:.2f}"
            "\nBest Harmonic: {}"
            "\nLengths: hist:{} gauss_hist:{} d_gauss_hist:{} FFT:{}"
            "\nNumber of lines:{} "
            "".format(
                self.path,
                self.ht, self.wd,
                self.imgarr.shape, self.closed.shape,
                self.angle, self.best_harmonic,
                len(self.hist), len(self.gauss_hist), len(self.d_gauss_hist),
                len(self.fft),
                self.num_lines))

        ret += "\nLine From  Top Base Till"
        for line in range(self.num_lines):
            ret += "\n{:3d}: {:4d} {:4d} {:4d} {:4d}".format(line,
                self.line_sep[line], self.top_lines[line],
                self.base_lines[line], self.line_sep[line+1])

        return ret

    def get_hists_info(self):
        return "Line Hist GHist DGHist" + \
               "\n".join(
            ["{:4d} {:7.2f} {:7.2f} {:7.2f}".format(l, i, j, k)
             for l, i, j, k in zip(
                range(self.ht), self.hist, self.gauss_hist, self.d_gauss_hist)])

    def get_image_with_hist(self, width):
        hist = width * self.gauss_hist / np.max(self.gauss_hist)
        appendage = np.full((self.ht, width), 255, dtype='uint8')
        for row, count in enumerate(hist.astype('int')):
            appendage[row, :count] = 0

        appendage = im.fromarray(appendage)
        appended_img = im.new('RGB', (self.wd + width, self.ht))
        appended_img.paste(self.img, (0, 0))
        appended_img.paste(appendage, (self.wd, 0))
        return appended_img

    def draw_lines(self, target):
        width = target.size[0]
        draw = id.Draw(target)

        def draw_lines(locations, col):
            for loc in locations:
                draw.line((0, loc, width, loc), fill=col, width=1)

        draw_lines(self.top_lines, (200, 200, 0))
        draw_lines(self.base_lines, (0, 255, 0))
        draw_lines(self.line_sep, (0, 0, 255))

        return target

    def get_image_with_hist_and_lines(self, width):
        appended_img = self.get_image_with_hist(width)
        return self.draw_lines(appended_img)

    def save_image_with_hist_and_lines(self, width):
        target_name = self.path[:-4] + ".png"
        appended_img = self.get_image_with_hist(width)
        self.draw_lines(appended_img).save(target_name)
        print("Saving:", target_name)


################################ UNIT TEST ################################

def main(image_name):
    page = Page(image_name)
    page.process()
    print(page.get_info())
    page.save_image_with_hist_and_lines(100)


if __name__ == '__main__':
    import sys
    main(sys.argv[1])