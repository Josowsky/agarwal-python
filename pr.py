import logging # This module is thread safe.
import threading
import pprint
from utils.getBinaryTree import getBinaryTree

logging.basicConfig(level=logging.INFO)
LOCK = threading.Lock()

NUMBER_OF_HOSTS = 16


def run(arg):
    if LOCK.acquire(False): # Non-blocking -- return whether we got it
        logging.info('Got the lock! {}'.format(arg))
        LOCK.release()
    else:
        logging.info("Couldn't get the lock. Maybe next time")


threads = []
for i in range(NUMBER_OF_HOSTS):
	threads.append(threading.Thread(target=run, args=[i]))

binary_tree = getBinaryTree(NUMBER_OF_HOSTS)

print binary_tree

# for thread in threads:
#    thread.start()
