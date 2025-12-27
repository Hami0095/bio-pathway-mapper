
# Placeholder for logging implementation
import logging

def get_logger(name):
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)
