import logging
import time

logfile_path = 'logs/' + str(time.strftime("%d-%m-%Y")) + '.log'
logging.basicConfig(filename=logfile_path, filemode='w', format='%(asctime)s %(levelname)s:%(message)s')

