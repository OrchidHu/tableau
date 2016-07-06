#codding:utf8
import logging
try:
    from local.local_config import *
except ImportError:
    logging.warning("No local_config file found.")

