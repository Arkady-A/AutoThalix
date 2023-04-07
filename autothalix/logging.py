import logging
import os
import sys
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


script_path = sys.argv[0]
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler = logging.FileHandler(os.path.join(os.path.dirname(script_path), 'experiment.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)