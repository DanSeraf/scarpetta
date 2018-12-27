import logging
from config import globalConfig

logger = None

def setupLogger():
    global logger
    err_log = logging.FileHandler(globalConfig()['project_dir'] + globalConfig()['log'])
    err_log.setLevel(logging.ERROR)
    logger = logging.getLogger('file')
    logger.addHandler(err_log)

def error(*args):
    from sys import stderr
    if logger is None:
        setupLogger()
    logger.error(args)
    print('\033[91m', args, '\033[0m', file=stderr)

def info(*args):
    if logger is None:
        setupLogger()
    print(args)
