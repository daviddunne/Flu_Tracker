import logging
import time
import os

current_dir_path = os.path.dirname(__file__)
logfile_path = os.path.join(current_dir_path, '../logs/' + str(time.strftime("%d-%m-%Y")) + '.log')
logging.basicConfig(filename=logfile_path, filemode='w', format='%(asctime)s %(levelname)s:%(message)s')

