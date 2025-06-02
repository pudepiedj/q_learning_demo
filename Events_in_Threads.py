# An Event manages an internal flag that callers can either set() or clear().
# Other threads can wait() for the flag to be set().
# Note that the wait() method blocks until the flag is true.

# Notice that 'logging.debug' tells you which part of the program you are in

import threading
import time
import logging

# filemode = 'w' overwrites log file rather than appending to it
logging.basicConfig(filename='example.log', filemode = 'w', level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
                    
def printing_counter(n):
    event_is_set = e.is_set()
    logging.debug('event set: %s', event_is_set)
    event_is_set = e.set()
    logging.debug('event set: %s', event_is_set)
    event_is_set = e.clear()
    logging.debug('event set: %s', event_is_set)
    for i in range(n):
        logging.debug("Counting %d", i)

def wait_for_event(e):
    logging.debug('wait_for_event starting - first line of wait_for_event')
    logging.debug('now we set event e which causes other threads to wait')
    event_is_set = e.wait()
    logging.debug('event set: %s', event_is_set)
    logging.debug('now this function rules the roost until it terminates')
    for i in range(3):
        logging.debug('Waiting inside WAIT_FOR_EVENT with event set for second %d', i)
        time.sleep(1)

def wait_for_event_timeout(e, t):
    while not e.isSet():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event because event is %s',event_is_set)
        else:
            logging.debug('doing other things because event is %s',event_is_set)

if __name__ == '__main__':
    e = threading.Event()

    logging.debug('Setting up the PRINTING_COUNTER thread')
    t0 = threading.Thread(name='COUNT_FUNCTION', 
                      target=printing_counter,
                      args=(20,))
    logging.debug('Starting the PRINTING_COUNTER thread')
    t0.start()
    
    logging.debug('Setting up the thread WAIT_FOR_EVENT')
    t1 = threading.Thread(name='wait_for_Event thread called BLOCKING', 
                      target=wait_for_event,
                      args=(e,))
    logging.debug('Starting the thread WAIT_FOR_EVENT')
    t1.start()
    
    logging.debug('Setting up the thread WAIT_FOR_EVENT_TIMEOUT')
    t2 = threading.Thread(name='wait_for_event_timeout thread called NON-BLOCKING', 
                      target=wait_for_event_timeout, 
                      args=(e, 2))
    logging.debug('Starting the thread WAIT_FOR_EVENT_TIMEOUT')
    t2.start()

    logging.debug('Waiting before calling Event.set()')
    for i in range(3):
        logging.debug('Waiting for second %d', i)
        time.sleep(1)
    logging.debug('Setting the EVENT')
    e.set()
    logging.debug('Event is set')
    logging.debug('Now what?') 
