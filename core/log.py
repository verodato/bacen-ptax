import logging.config
import os

'''
    Available Handlers Name
    root
    console
'''


def log(handler_name):
    logging.config.fileConfig(fname=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'settings.ini')))
    logger = logging.getLogger(handler_name)
    return logger