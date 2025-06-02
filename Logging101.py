# Learning about LOGGING

import logging

print("These two logs just go to the console:\n But the second doesn't because default logging level is WARNING")
logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything becasue INFO < WARNING

print("Now we reduce the level of severity we log to INFO and do it again:\n")

logging.basicConfig(level=logging.INFO)

logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # still will not print anything

print("Now we send the messages to a file called example.log")

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this, but not to the console')
logging.warning('And this, too')

print("These two logs again just go to the console:\n\n")

logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything


