import logging.handlers
import os
import shutil

from main import number_of_testers

LOG_FILENAME = 'logs/log'

if not os.path.exists('logs/'):
    os.makedirs('logs/')
else:
    shutil.rmtree('logs/')
    os.makedirs('logs/')

formatter = logging.Formatter('%(asctime)s - %(agent)s - %(message)s')

loggers = [None] * number_of_testers
db_handlers = [None] * number_of_testers

i = 0
while i < len(loggers):
    loggers[i] = logging.getLogger('Main logger ' + str(i))
    loggers[i].setLevel(logging.DEBUG)

    db_handlers[i] = logging.handlers.RotatingFileHandler(
        LOG_FILENAME + str(i) + ".out", maxBytes=10240 * 5, backupCount=5)
    db_handlers[i].setLevel(logging.DEBUG)
    db_handlers[i].setFormatter(formatter)
    loggers[i].addHandler(db_handlers[i])
    i += 1
