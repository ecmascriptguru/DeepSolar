import os
import sys


class Config(object):
    """Basic Configuration class for project
    """
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DEBUG = os.environ.get('DEBUG', False)
    TRAIN_SET_DIR_NAME = 'SPI_train'
