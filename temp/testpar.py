import Queue
import random
import threading
import time
import sys

data_queue = Queue.Queue()
lock = threading.Lock()


def gcd(a, b):
    while b != 0:
        a, b = b, a % b

    return a


def consumer(idnum):
    while True:
        try:
            data = data_queue.get(block=False)
        except Exception as e:
            print('Exception ' + str(e))
        else:
            with lock:
                print('\t consumer %d: computed gcd(%d, %d) = %d' % (
                idnum, data[0], data[1], gcd(data[0], data[1])))

        time.sleep(1)
        data_queue.task_done()


def producer(idnum, count):
    for i in range(count):
        a, b = random.randint(1, sys.maxint), random.randint(1, sys.maxint)
        with lock:
            print('\t producer %d: generated (%d, %d)' % (idnum, a, b))
        data_queue.put((a, b))
        time.sleep(0.5)


if __name__ == '__main__':
    num_producers = 1
    num_consumers = 2
    num_integer_pairs = 10

    for i in range(num_consumers):
        t = threading.Thread(target=consumer, args=(i,))
        t.daemon = True
        t.start()

    threads = []
    for ii in range(num_producers):
        thread = threading.Thread(target=producer, args=(ii, num_integer_pairs))
        threads.append(thread)
        thread.start()

    # wait for the producers threads to finish
    for thread in threads:
        thread.join()
    print
    'done with producer threads'

    # wait till all the jobs are done in the queue
    data_queue.join()

    with lock:
        print
        'all consumer threads finished'

    with lock:
        print
        'main thread exited'