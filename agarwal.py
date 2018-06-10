import time

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

# Put our process in the middle of hosts vector
middleElementIndex = getMiddleElement(hosts)
hosts[HOST_ID] = hosts[middleElementIndex]
hosts[middleElementIndex] = HOST_ID

# Create binary tree
binary_tree = getBinaryTree(hosts)

# Print binary tree
# print '===== GENERATED BINARY TREE ===='
# printTree(binary_tree)
# print '=====   =====   ===== \n\n'

# Get tree structured quorum
quorumSet = getQuorum(binary_tree)

# Prepare set of proces that need to accept request
replaySet = quorumSet
replaySet.remove(HOST_ID)
mpiInterface.quorumSet = replaySet

# Print tree structured quorum
# print '===== QUORUM ====='
# print '{}\n'.format(quorumSet)

# Request access to CS
if HOST_ID == 1:
    mpiInterface.request(HOST_ID, quorumSet)

while True:
    mpiInterface.listen()
    time.sleep(REFRESH_INTERVAL)
