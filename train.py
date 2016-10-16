import concurrent.futures as cf
import logging
import multiprocessing
import queue
import sys
import pickle
from datetime import datetime as dt

import theano as th
import numpy as np

import telugu as lang
import rnn_ctc.neuralnet as nn
import scribe
import utils


logger = logging.getLogger(__name__)
logi = logger.info
logd = logger.debug

###############################
# Initialize
args = utils.read_args(sys.argv[1:])
num_samples, num_epochs = args['num_samples'], args['num_epochs']
scribe_args, nnet_args = args['scribe_args'], args['nnet_args']

print('\nArguments:'
      '\nFloatX         : {}'
      '\nNum Epochs     : {}'
      '\nNum Samples    : {}'
      '\n'.format(th.config.floatX, num_epochs, num_samples))

scribe_args['dtype'] = th.config.floatX
scriber = scribe.Scribe(lang, **scribe_args)
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


def task():
    image, labels = scriber()
    labels_blanked = utils.insert_blanks(labels, lang.num_labels, num_blanks_at_start=2)
    # if len(y_blanked) < 2:
    #     print(y_blanked, end=' ')
    #     continue
    cst, pred, forward_probs = ntwk.trainer(image, labels_blanked)
    return image, labels, labels_blanked, cst, pred, forward_probs


max_workers = multiprocessing.cpu_count()
pool = cf.ProcessPoolExecutor(max_workers=max_workers)
task_queue = queue.Queue(max_workers * 2)


def queue_tasks():
    while not task_queue.full():
        task_queue.put(pool.submit(task))


def train_network():
    for epoch in range(num_epochs):
        ntwk.update_learning_rate(epoch)
        success = [0, 0]

        for samp in range(num_samples):
            queue_tasks()
            task = task_queue.get()
            x, y, y_blanked, cst, pred, forward_probs = task.result()

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

        print("Successes: {0[0]}/{0[1]}".format(success))
        successes.append(success)
        wts.append(ntwk.layers[0].params[1].get_value())

    with open(output_namer, 'wb') as f:
        pickle.dump((wts, successes), f, -1)
        print(output_namer)


if __name__ == '__main__':
    train_network()
