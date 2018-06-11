import time
from random import shuffle

from utils.mpi import MpiInterface as MPI
from utils.printTree import printTree
from utils.getBinaryTree import getBinaryTree, getMiddleElement
from utils.getQuorum import getQuorum

# Initialize mpi
mpiInterface = MPI()

# Constants
REFRESH_INTERVAL = 0.5
NUMBER_OF_HOSTS = mpiInterface.NUMBER_OF_HOSTS
HOST_ID = mpiInterface.HOST_ID

# # Create hosts vector
hosts = range(0, NUMBER_OF_HOSTS)

# Put our process in the middle of hosts vector and shiffle it
middleElementIndex = getMiddleElement(hosts)
del hosts[HOST_ID]
shuffle(hosts)
hosts.insert(middleElementIndex, HOST_ID)

# Create binary tree
binary_tree = getBinaryTree(hosts)

# Print binary tree
# print '===== GENERATED BINARY TREE ===='
# printTree(binary_tree)
# print '=====   =====   ===== \n\n'

# Get tree structured quorum
quorumSet = getQuorum(binary_tree)
mpiInterface.quorumSet = quorumSet

# Prepare set of proces that need to accept request
replySet = quorumSet[:]
replySet.remove(HOST_ID)
mpiInterface.replySet = replySet

# Print tree structured quorum
# print '===== QUORUM ====='
# print '{}\n'.format(quorumSet)

# Request access to CS
if HOST_ID == 1 or HOST_ID == 7 or HOST_ID == 12 or HOST_ID == 15:
    mpiInterface.request()

while True:
    mpiInterface.listen()
    time.sleep(REFRESH_INTERVAL)
