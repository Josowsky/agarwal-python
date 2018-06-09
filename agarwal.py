import logging
import threading
import pprint

from utils.printTree import printTree
from utils.getBinaryTree import getBinaryTree
from utils.getQuorum import getQuorum

logging.basicConfig(level=logging.INFO)
LOCK = threading.Lock()

# Constants
NUMBER_OF_HOSTS = 10


# Main execution function (probably will get depracated with MPI arival)
def run(arg):
    if LOCK.acquire(False): # Non-blocking -- return whether we got it
        logging.info('Got the lock! {}'.format(arg))
        LOCK.release()
    else:
        logging.info("Couldn't get the lock. Maybe next time")


threads = []
for i in range(NUMBER_OF_HOSTS):
	threads.append(threading.Thread(target=run, args=[i]))

# Create binary tree
binary_tree = getBinaryTree(NUMBER_OF_HOSTS)

# Print binary tree
print '===== GENERATED BINARY TREE ===='
printTree(binary_tree)
print '=====   =====   ===== \n\n'

# Get tree structured quorum
print getQuorum(binary_tree)

# for thread in threads:
#    thread.start()
