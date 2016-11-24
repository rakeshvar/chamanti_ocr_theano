from datetime import datetime as dt
import pickle
import sys

import numpy as np
import theano as th

import rnn_ctc.neuralnet as nn
#from parscribe import ParScribe as Scribe
from scribe import Scribe
import utils
import telugu as lang

################################ Initialize
args = utils.read_args(sys.argv[1:])
num_samples, num_epochs = args['num_samples'], args['num_epochs']
scribe_args, nnet_args = args['scribe_args'], args['nnet_args']

print('\nArguments:'
      '\nFloatX         : {}'
      '\nNum Epochs     : {}'
      '\nNum Samples    : {}'
      '\n'.format(th.config.floatX, num_epochs, num_samples))

scribe_args['dtype'] = th.config.floatX
scriber = Scribe(lang, **scribe_args)
printer = utils.Printer(lang.chars)
print(scriber)

print('Building the Network')
ntwk = nn.NeuralNet(scriber.height, lang.num_labels, **nnet_args)
print(ntwk)

try:
    output_namer = sys.argv[1]
except IndexError:
    output_namer = "default.ast"
output_namer = output_namer[:-4] + dt.now().strftime('%Y%m%d_%H%M') + '.pkl'
successes, wts = [], []
################################
print('Training the Network')
for epoch in range(num_epochs):
    ntwk.update_learning_rate(epoch)
    success = [0, 0]

    for samp in range(num_samples):
        x, y = scriber()
        y_blanked = utils.insert_blanks(y, lang.num_labels, num_blanks_at_start=2)
        # if len(y_blanked) < 2:
        #     print(y_blanked, end=' ')
        #     continue
        cst, pred, forward_probs = ntwk.trainer(x, y_blanked)

        if np.isinf(cst):
            printer.show_all(y, x, pred,
                             (forward_probs > 1e-20, 'Forward probabilities:', y_blanked))
            print('Exiting on account of Inf Cost...')
            break

        if samp == 0:   # or len(y) == 0:
            pred, hidden = ntwk.tester(x)

            print('Epoch:{:6d} Cost:{:.3f}'.format(epoch, float(cst)))
            printer.show_all(y, x, pred,
                             (forward_probs > -6, 'Forward probabilities:', y_blanked),
                             ((hidden + 1)/2, 'Hidden Layer:'))
            utils.pprint_probs(forward_probs)

        if len(y) > 1:
            success[0] += printer.decode(pred) == y
            success[1] += 1

    successes.append(success)
    wts.append(ntwk.layers[0].params[1].get_value())
    print("Successes: {0[0]}/{0[1]}".format(success))

with open(output_namer, 'wb') as f:
    pickle.dump((wts, successes), f, -1)
    print("Output is written to:", output_namer)
