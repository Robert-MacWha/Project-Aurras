import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import transformers
transformers.logging.set_verbosity_error()

import logging
logging.basicConfig(filename="logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

from .aurras import *