import logging
import threading
import time

import random

plot_x = []
plot_y = []

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    for i in range(10):
        print(name, i, "\n")
    logging.info("Thread %s: finishing", name)

def increment():
    for i in range(1000):
        plot_x.append(random.randint(0,20))
    print("Plot_x = ",plot_x)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=increment)
    y = threading.Thread(target=thread_function, args=(2,))
    z = threading.Thread(target=thread_function, args=(3,))
#    y.daemon = True
    logging.info("Main    : before running thread")
    x.start()
    y.start()
    z.start()
    logging.info("Main    : wait for the threads to finish")
    z.join()
    x.join()        # force the x-thread to finish; note that the y-thread doesn't
    logging.info("Main    : all done")
