import sys
import os
import logging
import logging.config
from logging.handlers import RotatingFileHandler

LOG = None

def get_logger():
    FILE_PATH = '/var/log/xx.log'
    logging.basicConfig(format = '[%(asctime)s] [%(levelname)s] %(message)s', 
            level = logging.INFO) 
    handlers = [ 
            RotatingFileHandler(FILE_PATH,
                mode='a',
                maxBytes = 10 * 1024 * 1024,
                backupCount = 5),
            ]   
    fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    logger = logging.getLogger()
    for handler in handlers:
        handler.setFormatter(fmt)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
    return logger

LOG = get_logger()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)

    level = sys.argv[1]
    msg = sys.argv[2]

    log = get_logger()

    if level.lower() == 'debug':
        log.debug(msg)
    if level.lower() == 'info':
        log.info(msg)
    if level.lower() == 'warning':
        log.warning(msg)
    if level.lower() == 'error':
        log.error(msg)
    if level.lower() == 'critical':
        log.critical(msg)

    sys.exit(0)


