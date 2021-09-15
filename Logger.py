import logging, IO_Helper, traceback
import logging.config

def getLogger(logger_name):

    log_file_name = 'logging/' + logger_name+ '.log'
    logger = logging.getLogger(log_file_name)
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    fileHandler = logging.FileHandler(log_file_name)
    consoleHandler.setLevel(logging.DEBUG)
    fileHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)
    # pass
    return logger