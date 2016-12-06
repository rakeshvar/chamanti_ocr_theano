import sys
from datetime import datetime as dt

import editdistance
import numpy as np
import theano as th

import rnn_ctc.neuralnet as nn
# from parscribe import ParScribe as Scribe
from scribe import Scribe
import utils
import telugu as lang
import utils

############################################ Read Args
args = utils.read_args(sys.argv[1:])
num_samples, num_epochs = args['num_samples'], args['num_epochs']
scribe_args, nnet_args = args['scribe_args'], args['nnet_args']

if len(sys.argv) > 1:
    output_fname = '-'.join(sorted(sys.argv[1:]))
    output_fname = output_fname.replace('.ast', '').replace('/', '').replace('configs', '')
else:
    output_fname = "default"
output_fname += '_' + dt.now().strftime('%y%m%d_%H%M') + '.txt'
distances, wts = [], []
print("Output will be written to: ", output_fname)

# Initialize Language
lang.select_labeler(args['labeler'])
alphabet_size = len(lang.symbols)

# Initialize Scriber
scribe_args['dtype'] = th.config.floatX
scriber = Scribe(lang, **scribe_args)
printer = utils.Printer(lang.symbols)

# Initialize the Neural Network
print('Building the Network')
ntwk = nn.NeuralNet(scriber.height, alphabet_size, **nnet_args)

# Print
print('\nArguments:')
utils.write_dict(args)
print('FloatX: {}'.format(th.config.floatX))
print('Alphabet Size: {}'.format(alphabet_size))

################################ Train
print('Training the Network')
for epoch in range(num_epochs):
    ntwk.update_learning_rate(epoch)
    edit_dist, tot_len = 0, 0

    for samp in range(num_samples):
        x, y = scriber.get_text_image()
        y_blanked = utils.insert_blanks(y, alphabet_size, num_blanks_at_start=2)
        # if len(y_blanked) < 2:
        #     print(y_blanked, end=' ')
        #     continue
        cst, pred, forward_probs = ntwk.trainer(x, y_blanked)

        if np.isinf(cst):
            printer.show_all(y, x, pred,
                             (forward_probs > 1e-20, 'Forward probabilities:', y_blanked))
            print('Exiting on account of Inf Cost...')
            break

        if samp == 0 and epoch==num_epochs-1:   # or len(y) == 0:
            pred, hidden = ntwk.tester(x)

            print('Epoch:{:6d} Cost:{:.3f}'.format(epoch, float(cst)))
            printer.show_all(y, x, pred,
                             (forward_probs > -6, 'Forward probabilities:', y_blanked),
                             ((hidden + 1)/2, 'Hidden Layer:'))
            utils.pprint_probs(forward_probs)

        edit_dist += editdistance.eval(printer.decode(pred), y)
        tot_len += len(y)

    distances.append((edit_dist, tot_len))
    # wts.append(ntwk.layers[0].params[1].get_value())
    # print("Successes: {0[0]}/{0[1]}".format(edit_dist))


################################ save
with open(output_fname, 'w') as f:
    # pickle.dump((wts, successes), f, -1)
    utils.write_dict(args, f)

    f.write("Edit Distances\n")
    for i, (e, t) in enumerate(distances):
        f.write("{:4d}: {:5d}/{:5d}\n".format(i, e, t))

print(output_fname, distances[-1])