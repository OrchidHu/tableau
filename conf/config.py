# coding=utf8

import logging

try:
    from local_config import *
    from db_config import *
except ImportError:
    logging.warning("No local_config file found.")
