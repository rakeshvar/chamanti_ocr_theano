import numpy as np
import theano as th
import theano.tensor as tt
from theano.ifelse import ifelse
_0 = np.cast[th.config.floatX](0)

####################### Log Space Helpers ################################
min_log = np.cast[th.config.floatX](-50)

def safe_log(x):
    return tt.maximum(tt.log(x), min_log)

def _log_add(x, y):
    maxx = tt.maximum(x, y)
    minn = tt.minimum(x, y)
    return maxx + tt.log(1 + tt.exp(minn - maxx))

def logadd(x, y, *zs):
    sum = _log_add(x, y)
    for z in zs:
        sum = _log_add(sum, z)
    return sum

def logmul(x, y):
    return x + y


####################### Two Kinds of CTC Layers ################################
"""
Recurrent Relation:
    Specifies allowed transistions in paths.

    Implemented as
        Matrix in PlainCTC
        Masks in LogCTC

    At any time, one could feed in from the
        0) same label
            - diagonal is identity (Plain)
        1) previous label
                (unless of course you are the first label)
            - first upper diagonal is identity (Plain)
            - prev_mask is [0, 1, 1, ..., 1] (Log)
        2) previous to previous label if
                a) previous label is blank and
                b) the previous to previous label is different from the current
            - second_diag/prevprev_mask is product of conditions a & b
"""


class CTCLayer():
    def __init__(self, inpt, labels, blank, log_space):
        """
        :param inpt: Output of Soft-max layer
        :param labels: desired/correct labels
        :param blank: index of blank
        :param log_space: If calcualtions should be done in log space
        :return: CTCLayer object
        """
        self.inpt = inpt
        self.labels = labels
        self.blank = blank
        self.n = self.labels.shape[0]
        if log_space:
            self._log_ctc()
        else:
            self._plain_ctc()
        self.params = []

    def _plain_ctc(self, ):
        labels2 = tt.concatenate((self.labels, [self.blank, self.blank]))
        sec_diag = tt.neq(labels2[:-2], labels2[2:]) * tt.eq(labels2[1:-1], self.blank)
        # Last two entries of sec_diag do not matter as they multiply zero rows below.

        recurrence_relation = \
            tt.eye(self.n) + \
            tt.eye(self.n, k=1) + \
            tt.eye(self.n, k=2) * sec_diag.dimshuffle((0, 'x'))

        pred_y = self.inpt[:, self.labels]

        fwd_pbblts, _ = th.scan(
            lambda curr, accum: curr * tt.dot(accum, recurrence_relation),
            sequences=[pred_y],
            outputs_info=[tt.eye(self.n)[0]]
        )

        # TODO: Add probabilites[-1, -2] only if last label is blank.
        # liklihood = ifelse(tt.eq(self.n, 1), fwd_pbblts[-1, -1],
        #                        ifelse(tt.neq(self.labels[-1], self.blank), fwd_pbblts[-1, -1],
        #                               fwd_pbblts[-1, -1] + fwd_pbblts[-1, -2]))
        liklihood = fwd_pbblts[-1, -1]
        self.cost = -tt.log(liklihood)
        self.debug = fwd_pbblts.T

    def _log_ctc(self, ):
        _1000 = tt.eye(self.n, dtype=th.config.floatX)[0]
        prev_mask = 1 - _1000
        prev_mask = safe_log(prev_mask)
        prevprev_mask = tt.neq(self.labels[:-2], self.labels[2:]) * \
                        tt.eq(self.labels[1:-1], self.blank)
        prevprev_mask = tt.concatenate(([0, 0], prevprev_mask)).astype(th.config.floatX)
        prevprev_mask = safe_log(prevprev_mask)
        prev = tt.arange(-1, self.n - 1)
        prevprev = tt.arange(-2, self.n - 2)
        log_pred_y = tt.log(self.inpt[:, self.labels])

        def step(curr, accum):
            return logmul(curr,
                          logadd(accum,
                                 logmul(prev_mask, accum[prev]),
                                 logmul(prevprev_mask, accum[prevprev])))

        log_fwd_pbblts, _ = th.scan(
            step,
            sequences=[log_pred_y],
            outputs_info=[safe_log(_1000)]
        )

        # TODO: Add probabilites[-1, -2] only if last label is blank.
        #     If length = 1, skip the scan process.
        # log_liklihood = ifelse(tt.eq(self.n, 1), tt.sum(log_pred_y),
        #                    ifelse(tt.eq(self.labels[-1], self.blank),
        #                           logadd(log_fwd_pbblts[-1, -1], log_fwd_pbblts[-1, -2]),
        #                           log_fwd_pbblts[-1, -1]))
        log_liklihood = log_fwd_pbblts[-1, -1]
        self.cost = -log_liklihood
        self.debug = log_fwd_pbblts.T