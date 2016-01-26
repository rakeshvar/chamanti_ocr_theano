import fonters
import labelers
import indic_scribe as ind
import random

class LineDraw():
    def __init__(self,
                 length=1,
                 tenn=5,
                 ht=36,
                 buf=5,
                 labeler_name="basic",
                 language="Telugu",
                 ):
        self.length = length
        self.tenn = tenn
        self.ht = ht
        self.buf = buf

        self.texter = None  # (length)
        self.labeler = labelers.get_labler_by_name(labeler_name)
        self.fonter = fonters.get_fonter_by_name(language)

    def get_line(self, length=None):
        twist = random.random()
        font_prop = self.fonter()

        text = self.texter.get(length)
        img = ind.scribe(text,
                         font_prop["font"],
                         size=font_prop["size"],
                         style=font_prop["style"],
                         twist=twist)

        img = ind.smartrim(img, self.ht, self.buf)

        return img, self.labeler(text)

    def set_length(self, length):
        self.length = length